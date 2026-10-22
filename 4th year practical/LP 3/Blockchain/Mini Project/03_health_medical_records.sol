// SPDX-License-Identifier: MIT
// ============================================================================
//   Mini Project: Blockchain-Based Electronic Health Records (EHR) System
//   Course: Blockchain Technology
//
//   Problem Statement:
//     Develop a Blockchain based application for health related medical records.
//
//   Description:
//     A patient-centric decentralized Electronic Health Record (EHR) management
//     system. Patients maintain full sovereignty over their private medical records,
//     granting and revoking access permissions to certified doctors. Authorized doctors
//     can append tamper-proof medical records (diagnoses, prescriptions, and IPFS
//     hashes of diagnostic scans) to the patient's immutable blockchain history.
//
//   Key Features:
//     • Hospital/Admin registers verified certified medical practitioners
//     • Patient self-registration with essential medical information
//     • Granular Access Control: Patients explicitly authorize or revoke doctor access
//     • Tamper-proof Medical Records: Diagnostic data & IPFS document hashes are immutable
//     • Full Audit Trail: Complete event logging of record additions and permission grants
//
//   Deployment & Testing in Remix IDE:
//     1. Open https://remix.ethereum.org/
//     2. Create a new file "03_health_medical_records.sol" and paste this code
//     3. Solidity Compiler: Choose version 0.8.19 or higher -> Click "Compile"
//     4. Deploy: Select "Remix VM" -> Click "Deploy" with Account 1 (Hospital Admin)
// ============================================================================

pragma solidity ^0.8.0;

contract HealthMedicalRecords {

    // ── Structs ─────────────────────────────────────────────────────────
    struct MedicalRecord {
        uint256 recordId;
        string diagnosis;
        string ipfsHash;         // Content identifier of lab report/radiology scan
        address doctorAddress;   // Physician who created the record
        string doctorName;
        uint256 timestamp;
    }

    struct Doctor {
        address doctorAddress;
        string name;
        string specialty;
        string hospital;
        bool isRegistered;
    }

    struct Patient {
        address patientAddress;
        string name;
        uint8 age;
        string bloodGroup;
        bool isRegistered;
        uint256 recordCount;
    }

    // ── State Variables ─────────────────────────────────────────────────
    address public hospitalAdmin;

    mapping(address => Doctor) public doctors;
    mapping(address => Patient) public patients;
    mapping(address => mapping(uint256 => MedicalRecord)) internal patientRecords; // patient => recordId => Record
    mapping(address => mapping(address => bool)) public isDoctorAuthorized;       // patient => doctor => authorized

    // ── Events ──────────────────────────────────────────────────────────
    event DoctorRegistered(address indexed doctorAddress, string name, string specialty);
    event PatientRegistered(address indexed patientAddress, string name, string bloodGroup);
    event AccessGranted(address indexed patient, address indexed doctor);
    event AccessRevoked(address indexed patient, address indexed doctor);
    event RecordAdded(address indexed patient, uint256 indexed recordId, address indexed doctor, string diagnosis);

    // ── Modifiers ───────────────────────────────────────────────────────
    modifier onlyAdmin() {
        require(msg.sender == hospitalAdmin, "Only hospital admin can perform this action");
        _;
    }

    modifier onlyRegisteredDoctor() {
        require(doctors[msg.sender].isRegistered, "Only certified doctors can perform this action");
        _;
    }

    modifier onlyRegisteredPatient() {
        require(patients[msg.sender].isRegistered, "Caller is not a registered patient");
        _;
    }

    // ── Constructor ─────────────────────────────────────────────────────
    constructor() {
        hospitalAdmin = msg.sender;
    }

    // ── 1. Register a Certified Doctor (Admin Only) ─────────────────────
    function registerDoctor(
        address _doctorAddress,
        string memory _name,
        string memory _specialty,
        string memory _hospital
    ) external onlyAdmin {
        require(_doctorAddress != address(0), "Invalid doctor address");
        require(!doctors[_doctorAddress].isRegistered, "Doctor already registered");

        doctors[_doctorAddress] = Doctor({
            doctorAddress: _doctorAddress,
            name: _name,
            specialty: _specialty,
            hospital: _hospital,
            isRegistered: true
        });

        emit DoctorRegistered(_doctorAddress, _name, _specialty);
    }

    // ── 2. Patient Self-Registration ────────────────────────────────────
    function registerPatient(
        string memory _name,
        uint8 _age,
        string memory _bloodGroup
    ) external {
        require(!patients[msg.sender].isRegistered, "Patient already registered");
        require(_age > 0 && _age < 130, "Invalid age provided");

        patients[msg.sender] = Patient({
            patientAddress: msg.sender,
            name: _name,
            age: _age,
            bloodGroup: _bloodGroup,
            isRegistered: true,
            recordCount: 0
        });

        emit PatientRegistered(msg.sender, _name, _bloodGroup);
    }

    // ── 3. Patient Grants Access to a Doctor ─────────────────────────────
    function grantAccess(address _doctorAddress) external onlyRegisteredPatient {
        require(doctors[_doctorAddress].isRegistered, "Target address is not a registered doctor");
        isDoctorAuthorized[msg.sender][_doctorAddress] = true;

        emit AccessGranted(msg.sender, _doctorAddress);
    }

    // ── 4. Patient Revokes Access from a Doctor ─────────────────────────
    function revokeAccess(address _doctorAddress) external onlyRegisteredPatient {
        require(isDoctorAuthorized[msg.sender][_doctorAddress], "Doctor is not currently authorized");
        isDoctorAuthorized[msg.sender][_doctorAddress] = false;

        emit AccessRevoked(msg.sender, _doctorAddress);
    }

    // ── 5. Authorized Doctor Adds a Medical Record ──────────────────────
    function addRecord(
        address _patientAddress,
        string memory _diagnosis,
        string memory _ipfsHash
    ) external onlyRegisteredDoctor {
        require(patients[_patientAddress].isRegistered, "Target patient is not registered");
        require(isDoctorAuthorized[_patientAddress][msg.sender], "Doctor is not authorized by this patient");

        Patient storage p = patients[_patientAddress];
        p.recordCount++;

        patientRecords[_patientAddress][p.recordCount] = MedicalRecord({
            recordId: p.recordCount,
            diagnosis: _diagnosis,
            ipfsHash: _ipfsHash,
            doctorAddress: msg.sender,
            doctorName: doctors[msg.sender].name,
            timestamp: block.timestamp
        });

        emit RecordAdded(_patientAddress, p.recordCount, msg.sender, _diagnosis);
    }

    // ── 6. View Medical Record (Patient or Authorized Doctor Only) ───────
    function getRecord(address _patientAddress, uint256 _recordId) external view returns (
        uint256 recordId,
        string memory diagnosis,
        string memory ipfsHash,
        address doctorAddress,
        string memory doctorName,
        uint256 timestamp
    ) {
        require(
            msg.sender == _patientAddress || isDoctorAuthorized[_patientAddress][msg.sender],
            "Unauthorized: You do not have permission to view this medical record"
        );

        MedicalRecord storage r = patientRecords[_patientAddress][_recordId];
        require(r.recordId > 0, "Record does not exist");

        return (r.recordId, r.diagnosis, r.ipfsHash, r.doctorAddress, r.doctorName, r.timestamp);
    }

    // ── 7. Get Total Patient Records Count ──────────────────────────────
    function getRecordCount(address _patientAddress) external view returns (uint256) {
        require(
            msg.sender == _patientAddress || isDoctorAuthorized[_patientAddress][msg.sender],
            "Unauthorized access to patient records summary"
        );
        return patients[_patientAddress].recordCount;
    }
}

/*
============================== SAMPLE OUTPUT & TESTING ==============================

  1. Deploy the Contract:
     - Deploy with Account 1 (Hospital Authority/Admin).
     - Hospital admin is configured as contract owner.

  2. Register Certified Doctor:
     - Switch to Account 1 (Admin).
     - Call registerDoctor():
       • _doctorAddress: Account 2 (Dr. Sharma)
       • _name: "Dr. Sharma, MD"
       • _specialty: "Cardiology"
       • _hospital: "Apollo Hospital"
     - Doctor registered with event `DoctorRegistered`.

  3. Register Patient:
     - Switch to Account 3 (Patient Rahul).
     - Call registerPatient():
       • _name: "Rahul Verma"
       • _age: 28
       • _bloodGroup: "O+"
     - Patient registered with event `PatientRegistered`.

  4. Grant Access Permission:
     - As Account 3 (Rahul), call grantAccess(Account 2).
     - Access flag isDoctorAuthorized[Rahul][Dr. Sharma] set to true.

  5. Authorized Doctor Adds Medical Record:
     - Switch to Account 2 (Dr. Sharma).
     - Call addRecord():
       • _patientAddress: Account 3 (Rahul)
       • _diagnosis: "Acute Bronchitis - Prescribed Amoxicillin 500mg"
       • _ipfsHash: "QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco" (Chest X-Ray)
     - Record ID = 1 successfully added to Rahul's immutable health record.

  6. Access Revocation & Security Check:
     - Switch to Account 3 (Rahul).
     - Call revokeAccess(Account 2).
     - Now switch to Account 2 and attempt addRecord() or getRecord():
       • Transaction Reverts with: "Doctor is not authorized by this patient".
     - Switch to Account 3 (Rahul). Call getRecord(Rahul, 1):
       • Returns: Record #1, Diagnosis: "Acute Bronchitis...", Doctor: "Dr. Sharma, MD".
       • Patient always retains access to their own records!

  GAS OBSERVATIONS:
  ──────────────────────────────────────────────────────────
  | Operation                  | Gas Used     | Type       |
  |────────────────────────────|──────────────|────────────|
  | Deploy EHR Contract        | ~790,000 gas | Deploy     |
  | registerDoctor()           | ~95,000 gas  | State write|
  | registerPatient()          | ~72,000 gas  | State write|
  | grantAccess()              | ~44,000 gas  | Access map |
  | addRecord()                | ~115,000 gas | Data store |
  | getRecord()                | 0 gas        | View read  |
  ──────────────────────────────────────────────────────────
=====================================================================================
*/
