/*
  Program 3: Bank Account Smart Contract
  Course: Blockchain Technology (LP-III)

  Problem Statement:
    Write a smart contract on a test network, for Bank account of a customer
    for following operations:
      - Deposit money
      - Withdraw money
      - Show balance
*/

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BankAccount {

    address public owner;
    mapping(address => uint256) private balances;

    event Deposited(address indexed account, uint256 amount, uint256 newBalance);
    event Withdrawn(address indexed account, uint256 amount, uint256 newBalance);

    constructor() {
        owner = msg.sender;
    }

    // Deposit money into customer's account
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");

        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value, balances[msg.sender]);
    }

    // Withdraw money from customer's account
    function withdraw(uint256 _amount) public {
        require(_amount > 0, "Withdrawal amount must be greater than zero");
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        balances[msg.sender] -= _amount;
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");

        emit Withdrawn(msg.sender, _amount, balances[msg.sender]);
    }

    // Show balance of the caller (view function -> 0 gas)
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    // Show total Ether held by the contract
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // Fallback to receive direct Ether transfers
    receive() external payable {
        balances[msg.sender] += msg.value;
    }
}

/*
  How to Test in Remix IDE:
  1. Open https://remix.ethereum.org/
  2. Create new file "BankAccount.sol" and paste this code.
  3. Compiler tab -> Select 0.8.x -> Click "Compile".
  4. Deploy tab -> Select "Remix VM" or "Injected Provider - MetaMask" (Sepolia testnet).
  5. Click "Deploy".
  6. Interact:
     - deposit(): Set Value to 1 Ether, click deposit.
     - getBalance(): Click to check balance in Wei (1 ETH = 10^18 Wei).
     - withdraw(): Enter amount in Wei to withdraw.
*/
