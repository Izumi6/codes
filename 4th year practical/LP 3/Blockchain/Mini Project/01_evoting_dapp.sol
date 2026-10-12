// SPDX-License-Identifier: MIT
// ============================================================================
//   Mini Project: E-Voting System (dApp)
//   Course: Blockchain Technology
//
//   Description:
//     A simple decentralized application (dApp) smart contract for an E-Voting 
//     system. It allows the admin to register voters and add candidates. 
//     Registered voters can cast one vote each. Anyone can view the results.
//
//   Features:
//     • Admin control (Owner only functions)
//     • Voter registration to prevent unauthorized voting
//     • Vote tracking to ensure one vote per registered user
//     • Transparent and immutable vote counting
//
//   Deployment & Testing:
//     1. Open Remix IDE: https://remix.ethereum.org/
//     2. Create a new file "EVoting.sol" → Paste this code
//     3. Compile: Select Solidity compiler 0.8.x → Compile
//     4. Deploy: Environment → "Remix VM"
// ============================================================================

pragma solidity ^0.8.0;

contract EVoting {

    // ── State Variables ────────────────────────────────────────────────
    address public admin;          // The deployer of the contract
    uint256 public totalVotes;     // Total number of votes cast

    // ── Structures ─────────────────────────────────────────────────────
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }

    struct Voter {
        bool isRegistered;
        bool hasVoted;
        uint256 votedCandidateId;
    }

    // ── Mappings & Arrays ──────────────────────────────────────────────
    mapping(uint256 => Candidate) public candidates;   // id -> Candidate
    mapping(address => Voter) public voters;           // address -> Voter

    uint256 public candidatesCount;

    // ── Events ─────────────────────────────────────────────────────────
    event CandidateAdded(uint256 candidateId, string name);
    event VoterRegistered(address voter);
    event VoteCast(address voter, uint256 candidateId);

    // ── Modifiers ──────────────────────────────────────────────────────
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only the admin can perform this action");
        _;
    }

    // ── Constructor ────────────────────────────────────────────────────
    constructor() {
        admin = msg.sender;
    }

    // ── Admin Functions ────────────────────────────────────────────────

    // 1. Add a new candidate
    function addCandidate(string memory _name) public onlyAdmin {
        candidatesCount++;
        candidates[candidatesCount] = Candidate({
            id: candidatesCount,
            name: _name,
            voteCount: 0
        });

        emit CandidateAdded(candidatesCount, _name);
    }

    // 2. Register a new voter
    function registerVoter(address _voter) public onlyAdmin {
        require(!voters[_voter].isRegistered, "Voter is already registered");
        
        voters[_voter].isRegistered = true;
        voters[_voter].hasVoted = false;

        emit VoterRegistered(_voter);
    }

    // ── Voter Functions ────────────────────────────────────────────────

    // 3. Cast a vote
    function castVote(uint256 _candidateId) public {
        // Validation checks
        require(voters[msg.sender].isRegistered, "You are not a registered voter");
        require(!voters[msg.sender].hasVoted, "You have already voted");
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID");

        // Record the vote
        voters[msg.sender].hasVoted = true;
        voters[msg.sender].votedCandidateId = _candidateId;

        // Update candidate's vote count
        candidates[_candidateId].voteCount++;
        totalVotes++;

        emit VoteCast(msg.sender, _candidateId);
    }

    // ── View Functions (No Gas Cost) ───────────────────────────────────

    // 4. View candidate details
    function getCandidate(uint256 _candidateId) public view returns (string memory name, uint256 voteCount) {
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID");
        
        Candidate memory c = candidates[_candidateId];
        return (c.name, c.voteCount);
    }

    // 5. Check if address has voted
    function hasAddressVoted(address _voter) public view returns (bool) {
        return voters[_voter].hasVoted;
    }
}

/*
============================== HOW TO TEST IN REMIX ==============================

  1. Deploy the Contract:
     - Make sure Account 1 is selected in Remix. Click "Deploy".
     - Account 1 becomes the `admin`.

  2. Add Candidates (Admin Only):
     - In deployed contract, find `addCandidate`.
     - Enter "Alice" -> Click transact.
     - Enter "Bob" -> Click transact.
     - (Optional) Verify by calling `candidatesCount`. It should return 2.

  3. Register a Voter (Admin Only):
     - Copy the address of Account 2 from the top dropdown.
     - Switch back to Account 1 (Admin).
     - Paste Account 2's address into `registerVoter` and transact.

  4. Cast a Vote:
     - Switch to Account 2 (the registered voter).
     - Enter "1" (for Alice) into `castVote` -> Click transact.
     - Try voting again with Account 2 -> It will fail ("You have already voted").
     - Try voting with Account 3 -> It will fail ("You are not a registered voter").

  5. View Results:
     - Enter "1" in `getCandidate` -> Returns ("Alice", 1).
     - Enter "2" in `getCandidate` -> Returns ("Bob", 0).
     - Click `totalVotes` -> Returns 1.

  GAS OBSERVATIONS:
  ─────────────────────────────────────────────────────────
  | Operation         | Gas Used    | Description        |
  |───────────────────|─────────────|────────────────────|
  | Deploy            | ~750,000    | Contract creation  |
  | addCandidate()    | ~110,000    | Writes to mapping  |
  | registerVoter()   | ~45,000     | Writes boolean     |
  | castVote()        | ~70,000     | Updates 3 states   |
  | getCandidate()    | 0           | View function      |
  ─────────────────────────────────────────────────────────

========================================================================
*/
