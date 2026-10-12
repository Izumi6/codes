// SPDX-License-Identifier: MIT
// ============================================================================
//   Program 3: Bank Account Smart Contract
//   Course: Blockchain Technology
//
//   Description:
//     Smart contract for a Bank account with the following operations:
//       • Deposit money
//       • Withdraw money
//       • Show balance
//
//   Deployment:
//     1. Open Remix IDE: https://remix.ethereum.org/
//     2. Create a new file → Paste this code
//     3. Compile: Select Solidity compiler 0.8.x → Compile
//     4. Deploy: Environment → "Injected Provider - MetaMask" (Sepolia testnet)
//        OR use "Remix VM" for local testing without MetaMask
//     5. Interact with deployed contract using the buttons in Remix
//
//   Observations:
//     • Deposit: Costs ~45,000-65,000 gas (writes to storage)
//     • Withdraw: Costs ~30,000-35,000 gas (storage update + ETH transfer)
//     • getBalance: Costs 0 gas (view function, read-only)
//     • Gas Fee = Gas Used × Gas Price (in Gwei)
// ============================================================================

pragma solidity ^0.8.0;

contract BankAccount {

    // ── State Variables ────────────────────────────────────────────────
    address public owner;                          // Owner of the bank contract
    mapping(address => uint256) private balances;  // Customer balances

    // ── Events ─────────────────────────────────────────────────────────
    // Events are emitted to log transaction details on the blockchain
    event Deposited(address indexed account, uint256 amount, uint256 newBalance);
    event Withdrawn(address indexed account, uint256 amount, uint256 newBalance);

    // ── Constructor ────────────────────────────────────────────────────
    // Runs once when the contract is deployed
    constructor() {
        owner = msg.sender;  // The deployer becomes the owner
    }

    // ── Deposit Function ───────────────────────────────────────────────
    // Allows anyone to deposit Ether into their account
    // The 'payable' keyword allows this function to receive Ether
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");

        balances[msg.sender] += msg.value;

        emit Deposited(msg.sender, msg.value, balances[msg.sender]);
    }

    // ── Withdraw Function ──────────────────────────────────────────────
    // Allows a customer to withdraw Ether from their account
    function withdraw(uint256 _amount) public {
        require(_amount > 0, "Withdrawal amount must be greater than zero");
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        balances[msg.sender] -= _amount;

        // Transfer Ether back to the customer
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");

        emit Withdrawn(msg.sender, _amount, balances[msg.sender]);
    }

    // ── Show Balance Function ──────────────────────────────────────────
    // Returns the balance of the caller
    // 'view' keyword means this function does NOT modify state (0 gas cost)
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    // ── Get Contract's Total Balance ───────────────────────────────────
    // Shows total Ether held by this contract
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // ── Receive Ether ──────────────────────────────────────────────────
    // Fallback to accept direct Ether transfers to the contract
    receive() external payable {
        balances[msg.sender] += msg.value;
    }
}

/*
============================== HOW TO TEST IN REMIX ==============================

  1. Open https://remix.ethereum.org/
  2. Create new file "BankAccount.sol" → Paste this code
  3. Compile: Solidity Compiler tab → Select 0.8.x → Click "Compile"
  4. Deploy: Deploy tab → Environment: "Remix VM (Shanghai)"
  5. Click "Deploy"

  TESTING:
  ─────────────────────────────────────────────────────────
  a) DEPOSIT:
     - In "VALUE" field (top), enter "1" and select "Ether"
     - Click "deposit" button
     - Observe: Transaction costs ~46,000 gas

  b) CHECK BALANCE:
     - Click "getBalance"
     - Shows: 1000000000000000000 (1 ETH in Wei)
     - This is a VIEW function → 0 gas cost

  c) WITHDRAW:
     - Enter amount in Wei: 500000000000000000 (0.5 ETH)
     - Click "withdraw"
     - Observe: Transaction costs ~31,000 gas

  d) CHECK BALANCE AGAIN:
     - Click "getBalance"
     - Shows: 500000000000000000 (0.5 ETH remaining)

  GAS OBSERVATIONS:
  ─────────────────────────────────────────────────────────
  | Operation       | Gas Used  | Gas Cost (at 20 Gwei) |
  |─────────────────|───────────|───────────────────────|
  | Deploy          | ~350,000  | 0.007 ETH             |
  | deposit()       | ~46,000   | 0.00092 ETH           |
  | withdraw()      | ~31,000   | 0.00062 ETH           |
  | getBalance()    | 0         | Free (view function)  |
  ─────────────────────────────────────────────────────────

  Note: 1 ETH = 10^18 Wei = 10^9 Gwei

========================================================================
*/
