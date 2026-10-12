// SPDX-License-Identifier: MIT
// ============================================================================
//   Program 4: Student Data Smart Contract
//   Course: Blockchain Technology
//
//   Description:
//     Smart contract to create and manage Student data using:
//       • Structures (struct) — to define student record
//       • Arrays — to store multiple students
//       • Fallback function — to handle unexpected calls
//
//   Deployment:
//     1. Open Remix IDE: https://remix.ethereum.org/
//     2. Create a new file → Paste this code
//     3. Compile: Select Solidity compiler 0.8.x → Compile
//     4. Deploy: Environment → "Injected Provider - MetaMask" (Sepolia)
//        OR use "Remix VM" for local testing
//     5. Observe gas values for each operation
//
//   Observations:
//     • addStudent: ~80,000-120,000 gas (writes struct + array push)
//     • getStudent: 0 gas (view function)
//     • getStudentCount: 0 gas (view function)
//     • Fallback: Triggered when unknown function is called
// ============================================================================

pragma solidity ^0.8.0;

contract StudentData {

    // ── Structure ──────────────────────────────────────────────────────
    // Struct to define the Student record
    struct Student {
        uint256 rollNo;       // Roll number
        string name;          // Student name
        uint256 age;          // Age
        string department;    // Department/Branch
    }

    // ── Array ──────────────────────────────────────────────────────────
    // Dynamic array to store all student records
    Student[] public students;

    // ── Events ─────────────────────────────────────────────────────────
    event StudentAdded(uint256 indexed rollNo, string name, string department);
    event FallbackCalled(address sender, uint256 value, bytes data);

    // ── Add Student Function ───────────────────────────────────────────
    // Adds a new student to the array
    function addStudent(
        uint256 _rollNo,
        string memory _name,
        uint256 _age,
        string memory _department
    ) public {
        // Create a new Student struct and push to array
        Student memory newStudent = Student({
            rollNo: _rollNo,
            name: _name,
            age: _age,
            department: _department
        });

        students.push(newStudent);

        emit StudentAdded(_rollNo, _name, _department);
    }

    // ── Get Student by Index ───────────────────────────────────────────
    // Returns student details at a given index
    // 'view' function → 0 gas cost (read-only)
    function getStudent(uint256 _index) public view returns (
        uint256 rollNo,
        string memory name,
        uint256 age,
        string memory department
    ) {
        require(_index < students.length, "Student index out of bounds");

        Student memory s = students[_index];
        return (s.rollNo, s.name, s.age, s.department);
    }

    // ── Get Total Student Count ────────────────────────────────────────
    // Returns the total number of students stored
    function getStudentCount() public view returns (uint256) {
        return students.length;
    }

    // ── Get All Students ───────────────────────────────────────────────
    // Returns all student records (useful for display)
    function getAllStudents() public view returns (Student[] memory) {
        return students;
    }

    // ── Fallback Function ──────────────────────────────────────────────
    // Called when a function that doesn't exist is called
    // OR when the contract receives data that doesn't match any function
    fallback() external payable {
        emit FallbackCalled(msg.sender, msg.value, msg.data);
    }

    // ── Receive Function ───────────────────────────────────────────────
    // Called when contract receives plain Ether with no data
    receive() external payable {
        emit FallbackCalled(msg.sender, msg.value, "");
    }
}

/*
============================== HOW TO TEST IN REMIX ==============================

  1. Open https://remix.ethereum.org/
  2. Create new file "StudentData.sol" → Paste this code
  3. Compile: Solidity Compiler tab → Select 0.8.x → Click "Compile"
  4. Deploy: Deploy tab → Environment: "Remix VM (Shanghai)"
  5. Click "Deploy"

  TESTING:
  ─────────────────────────────────────────────────────────
  a) ADD STUDENT:
     - Click "addStudent" → Enter parameters:
       _rollNo: 101
       _name: "Suyash"
       _age: 21
       _department: "Computer Engineering"
     - Click "transact"
     - Observe Gas: ~100,000 gas

  b) ADD ANOTHER STUDENT:
     - _rollNo: 102, _name: "Rahul", _age: 22, _department: "IT"
     - Observe Gas: ~95,000 gas (slightly less, storage already initialized)

  c) GET STUDENT:
     - Click "getStudent" → Enter index: 0
     - Returns: (101, "Suyash", 21, "Computer Engineering")
     - Gas: 0 (view function)

  d) GET STUDENT COUNT:
     - Click "getStudentCount"
     - Returns: 2
     - Gas: 0 (view function)

  e) TEST FALLBACK:
     - In "Low level interactions" section at bottom of deployed contract
     - Enter some hex data (e.g., 0x1234) in CALLDATA field
     - Click "Transact"
     - The fallback function will be triggered
     - Check logs → FallbackCalled event emitted

  TRANSACTION FEE & GAS OBSERVATIONS:
  ─────────────────────────────────────────────────────────
  | Operation         | Gas Used    | Cost (at 20 Gwei)  |
  |───────────────────|─────────────|────────────────────|
  | Deploy Contract   | ~800,000    | 0.016 ETH          |
  | addStudent()      | ~100,000    | 0.002 ETH          |
  | getStudent()      | 0           | Free (view)        |
  | getStudentCount() | 0           | Free (view)        |
  | Fallback trigger  | ~22,000     | 0.00044 ETH        |
  ─────────────────────────────────────────────────────────

  KEY OBSERVATIONS:
  1. Writing to storage (addStudent) is the most expensive operation.
  2. Reading from storage (view functions) is free.
  3. The first write to a storage slot costs more than subsequent writes.
  4. String storage is more expensive than uint256 storage.
  5. Fallback function is triggered for unrecognized function calls.
  6. Total Transaction Fee = Gas Used × Gas Price (in Gwei).

========================================================================
*/
