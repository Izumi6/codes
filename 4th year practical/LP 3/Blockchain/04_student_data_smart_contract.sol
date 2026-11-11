/*
  Program 4: Student Data Smart Contract
  Course: Blockchain Technology (LP-III)

  Problem Statement:
    Write a program in Solidity to create Student data. Use the following constructs:
      - Structures
      - Arrays
      - Fallback
    Deploy this as smart contract on Ethereum and observe transaction fee and gas values.
*/

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StudentData {

    // Structure
    struct Student {
        uint256 rollNo;
        string name;
        uint256 age;
        string department;
    }

    // Dynamic Array
    Student[] public students;

    event StudentAdded(uint256 indexed rollNo, string name, string department);
    event FallbackCalled(address sender, uint256 value, bytes data);

    // Add a new student record
    function addStudent(
        uint256 _rollNo,
        string memory _name,
        uint256 _age,
        string memory _department
    ) public {
        Student memory newStudent = Student({
            rollNo: _rollNo,
            name: _name,
            age: _age,
            department: _department
        });

        students.push(newStudent);
        emit StudentAdded(_rollNo, _name, _department);
    }

    // Get student details by index
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

    // Get total number of students
    function getStudentCount() public view returns (uint256) {
        return students.length;
    }

    // Get all students
    function getAllStudents() public view returns (Student[] memory) {
        return students;
    }

    // Fallback function: called when unknown function is called with data
    fallback() external payable {
        emit FallbackCalled(msg.sender, msg.value, msg.data);
    }

    // Receive function: called on plain Ether transfers
    receive() external payable {
        emit FallbackCalled(msg.sender, msg.value, "");
    }
}

/*
  How to Test in Remix IDE:
  1. Open https://remix.ethereum.org/
  2. Create new file "StudentData.sol" and paste this code.
  3. Compiler tab -> Select 0.8.x -> Click "Compile".
  4. Deploy tab -> Select "Remix VM" or "Injected Provider - MetaMask" (Sepolia testnet).
  5. Click "Deploy".
  6. Interact:
     - addStudent(1, "Suyash", 21, "Comp"): Transact (~95,000 - 100,000 gas).
     - getStudent(0): View function (0 gas).
     - getStudentCount(): View function (0 gas).
     - Low level interaction / calldata: Triggers fallback function.
*/
