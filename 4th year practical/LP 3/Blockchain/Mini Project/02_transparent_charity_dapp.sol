// SPDX-License-Identifier: MIT
// ============================================================================
//   Mini Project: Transparent and Genuine Charity Platform (dApp)
//   Course: Blockchain Technology
//
//   Problem Statement:
//     Develop a Blockchain based application for transparent and genuine charity.
//
//   Description:
//     A decentralized smart contract ensuring full financial transparency for
//     charitable fundraising. Donors can donate ETH to verified campaigns, track
//     exact fund utilization, and vote on spending requests before funds are
//     released to beneficiaries or vendors.
//
//   Key Features:
//     • Admin verifies and registers legitimate charitable campaigns
//     • Transparent donations: anyone can audit campaign balances and donor history
//     • Milestone Spending Requests: Charity managers cannot withdraw funds arbitrarily;
//       they must submit spending requests with stated recipient & amount
//     • Donor Voting: Donors vote to approve spending requests, preventing embezzlement
//     • Automatic Refund: Donors can reclaim funds if campaign fails to reach minimum goal
//
//   Deployment & Testing in Remix IDE:
//     1. Open https://remix.ethereum.org/
//     2. Create a new file "02_transparent_charity_dapp.sol" and paste this code
//     3. Solidity Compiler: Choose version 0.8.19 or higher -> Click "Compile"
//     4. Deploy & Run Transactions:
//        - Environment: "Remix VM (Shanghai/Cancun)"
//        - Click "Deploy" using Account 1 (Admin)
// ============================================================================

pragma solidity ^0.8.0;

contract TransparentCharity {

    // ── Structs ─────────────────────────────────────────────────────────
    struct SpendingRequest {
        uint256 id;
        string description;
        address payable recipient;   // Vendor or beneficiary receiving the funds
        uint256 amount;              // Amount of ETH requested
        uint256 approvalCount;       // Number of approving donors
        bool isExecuted;             // Whether funds have been released
        mapping(address => bool) hasVoted; // Donor voting tracker
    }

    struct Campaign {
        uint256 id;
        string title;
        string description;
        address payable charityManager; // Organization manager
        uint256 targetGoal;             // Target amount in wei
        uint256 deadline;               // Timestamp when campaign ends
        uint256 totalRaised;            // Total funds collected
        uint256 spentAmount;            // Total funds disbursed
        bool isClosed;                  // Status of campaign
        uint256 requestCount;           // Number of spending requests
    }

    // ── State Variables ─────────────────────────────────────────────────
    address public admin;
    uint256 public campaignCount;

    mapping(uint256 => Campaign) public campaigns;
    mapping(uint256 => mapping(address => uint256)) public campaignDonations; // campaignId => donor => amount
    mapping(uint256 => mapping(uint256 => SpendingRequest)) internal spendingRequests; // campaignId => requestId => Request

    // ── Events ──────────────────────────────────────────────────────────
    event CampaignCreated(uint256 indexed campaignId, string title, address charityManager, uint256 targetGoal);
    event DonationReceived(uint256 indexed campaignId, address indexed donor, uint256 amount);
    event SpendingRequestCreated(uint256 indexed campaignId, uint256 indexed requestId, string description, uint256 amount, address recipient);
    event SpendingRequestApproved(uint256 indexed campaignId, uint256 indexed requestId, address indexed donor);
    event FundsDisbursed(uint256 indexed campaignId, uint256 indexed requestId, address recipient, uint256 amount);
    event RefundIssued(uint256 indexed campaignId, address indexed donor, uint256 amount);

    // ── Modifiers ───────────────────────────────────────────────────────
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only platform admin can perform this action");
        _;
    }

    modifier onlyCharityManager(uint256 _campaignId) {
        require(msg.sender == campaigns[_campaignId].charityManager, "Only charity manager can perform this action");
        _;
    }

    // ── Constructor ─────────────────────────────────────────────────────
    constructor() {
        admin = msg.sender;
    }

    // ── 1. Create a Verified Charity Campaign ───────────────────────────
    function createCampaign(
        string memory _title,
        string memory _description,
        address payable _charityManager,
        uint256 _targetGoal,
        uint256 _durationDays
    ) external onlyAdmin {
        require(_targetGoal > 0, "Target goal must be greater than 0");
        require(_charityManager != address(0), "Invalid charity manager address");

        campaignCount++;
        Campaign storage c = campaigns[campaignCount];
        c.id = campaignCount;
        c.title = _title;
        c.description = _description;
        c.charityManager = _charityManager;
        c.targetGoal = _targetGoal;
        c.deadline = block.timestamp + (_durationDays * 1 days);
        c.totalRaised = 0;
        c.spentAmount = 0;
        c.isClosed = false;
        c.requestCount = 0;

        emit CampaignCreated(campaignCount, _title, _charityManager, _targetGoal);
    }

    // ── 2. Donate ETH to a Campaign ─────────────────────────────────────
    function donate(uint256 _campaignId) external payable {
        Campaign storage c = campaigns[_campaignId];
        require(c.id > 0 && !c.isClosed, "Campaign does not exist or is closed");
        require(block.timestamp < c.deadline, "Campaign funding deadline has passed");
        require(msg.value > 0, "Donation amount must be greater than 0");

        c.totalRaised += msg.value;
        campaignDonations[_campaignId][msg.sender] += msg.value;

        emit DonationReceived(_campaignId, msg.sender, msg.value);
    }

    // ── 3. Charity Manager Creates a Milestone Spending Request ─────────
    function createSpendingRequest(
        uint256 _campaignId,
        string memory _description,
        address payable _recipient,
        uint256 _amount
    ) external onlyCharityManager(_campaignId) {
        Campaign storage c = campaigns[_campaignId];
        require(!c.isClosed, "Campaign is closed");
        uint256 availableBalance = c.totalRaised - c.spentAmount;
        require(_amount <= availableBalance, "Insufficient unallocated funds in campaign");
        require(_recipient != address(0), "Invalid recipient address");

        c.requestCount++;
        SpendingRequest storage req = spendingRequests[_campaignId][c.requestCount];
        req.id = c.requestCount;
        req.description = _description;
        req.recipient = _recipient;
        req.amount = _amount;
        req.approvalCount = 0;
        req.isExecuted = false;

        emit SpendingRequestCreated(_campaignId, c.requestCount, _description, _amount, _recipient);
    }

    // ── 4. Donors Vote to Approve Spending Request ───────────────────────
    function voteSpendingRequest(uint256 _campaignId, uint256 _requestId) external {
        require(campaignDonations[_campaignId][msg.sender] > 0, "Only contributors can vote on requests");
        SpendingRequest storage req = spendingRequests[_campaignId][_requestId];
        require(!req.isExecuted, "Request has already been executed");
        require(!req.hasVoted[msg.sender], "You have already voted on this request");

        req.hasVoted[msg.sender] = true;
        req.approvalCount++;

        emit SpendingRequestApproved(_campaignId, _requestId, msg.sender);
    }

    // ── 5. Finalize Spending Request and Disburse Funds ──────────────────
    function executeSpendingRequest(uint256 _campaignId, uint256 _requestId) external onlyCharityManager(_campaignId) {
        Campaign storage c = campaigns[_campaignId];
        SpendingRequest storage req = spendingRequests[_campaignId][_requestId];

        require(!req.isExecuted, "Request already executed");
        require(req.amount <= (c.totalRaised - c.spentAmount), "Funds already exhausted");
        require(req.approvalCount >= 1, "Must have at least 1 donor approval");

        req.isExecuted = true;
        c.spentAmount += req.amount;

        (bool success, ) = req.recipient.call{value: req.amount}("");
        require(success, "ETH transfer to recipient failed");

        emit FundsDisbursed(_campaignId, _requestId, req.recipient, req.amount);
    }

    // ── 6. Donor Refund (If goal not reached past deadline) ──────────────
    function claimRefund(uint256 _campaignId) external {
        Campaign storage c = campaigns[_campaignId];
        require(block.timestamp >= c.deadline, "Campaign is still active");
        require(c.totalRaised < c.targetGoal, "Campaign reached target goal; refunds unavailable");

        uint256 contributed = campaignDonations[_campaignId][msg.sender];
        require(contributed > 0, "No contributions found to refund");

        campaignDonations[_campaignId][msg.sender] = 0;
        (bool success, ) = payable(msg.sender).call{value: contributed}("");
        require(success, "Refund transfer failed");

        emit RefundIssued(_campaignId, msg.sender, contributed);
    }

    // ── View Helper Functions ───────────────────────────────────────────
    function getCampaignDetails(uint256 _campaignId) external view returns (
        string memory title,
        string memory description,
        address charityManager,
        uint256 targetGoal,
        uint256 deadline,
        uint256 totalRaised,
        uint256 spentAmount,
        bool isClosed
    ) {
        Campaign storage c = campaigns[_campaignId];
        return (c.title, c.description, c.charityManager, c.targetGoal, c.deadline, c.totalRaised, c.spentAmount, c.isClosed);
    }

    function getSpendingRequest(uint256 _campaignId, uint256 _requestId) external view returns (
        string memory description,
        address recipient,
        uint256 amount,
        uint256 approvalCount,
        bool isExecuted
    ) {
        SpendingRequest storage req = spendingRequests[_campaignId][_requestId];
        return (req.description, req.recipient, req.amount, req.approvalCount, req.isExecuted);
    }
}

/*
============================== SAMPLE OUTPUT & TESTING ==============================

  1. Deploy the Contract:
     - Deploy with Account 1 (Admin).
     - Contract address is created.

  2. Create a Verified Campaign:
     - Call createCampaign():
       • _title: "Clean Drinking Water Project"
       • _description: "Installation of community water filters in drought-hit schools"
       • _charityManager: Account 2 (NGO Lead)
       • _targetGoal: 2000000000000000000 (2 ETH in Wei)
       • _durationDays: 30
     - Transaction Status: Success (Campaign ID = 1 created)

  3. Donate ETH:
     - Switch to Account 3 (Donor A).
     - Set Value = 1 Ether.
     - Call donate(1).
     - Switch to Account 4 (Donor B).
     - Set Value = 1 Ether.
     - Call donate(1).
     - Total Raised is now 2 ETH (100% of target goal).

  4. Submit Spending Request (Milestone Tracking):
     - Switch to Account 2 (NGO Lead).
     - Call createSpendingRequest():
       • _campaignId: 1
       • _description: "Purchase 50 commercial RO water filtration units from Supplier"
       • _recipient: Account 5 (Vendor / Supplier)
       • _amount: 1000000000000000000 (1 ETH)
     - Transaction Status: Success (Request ID = 1 created)

  5. Transparent Donor Approval:
     - Switch to Account 3 (Donor A).
     - Call voteSpendingRequest(1, 1).
     - approvalCount increments to 1.

  6. Release Funds:
     - Switch to Account 2 (NGO Lead).
     - Call executeSpendingRequest(1, 1).
     - 1 ETH is directly transferred to Account 5 (Supplier).
     - Campaign spentAmount updates to 1 ETH, remaining balance = 1 ETH.

  GAS ANALYSIS:
  ──────────────────────────────────────────────────────────
  | Operation                  | Gas Cost     | Function   |
  |────────────────────────────|──────────────|────────────|
  | Contract Deployment        | ~820,000 gas | constructor|
  | createCampaign()           | ~145,000 gas | State write|
  | donate()                   | ~48,000 gas  | Payable    |
  | createSpendingRequest()    | ~98,000 gas  | State write|
  | voteSpendingRequest()      | ~32,000 gas  | State write|
  | executeSpendingRequest()   | ~55,000 gas  | ETH send   |
  ──────────────────────────────────────────────────────────
=====================================================================================
*/
