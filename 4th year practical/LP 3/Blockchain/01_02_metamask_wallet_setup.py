"""
================================================================================
  Program 1 & 2: MetaMask Installation, Wallet Creation & Ether Transactions
  Course: Blockchain Technology

  Description:
    This document covers:
      1. Installation of MetaMask and studying Ether spending per transaction.
      2. Creating your own wallet using MetaMask for crypto transactions.

  No code execution needed — This is a step-by-step practical guide.
  All steps are performed in the browser using the MetaMask extension.
================================================================================
"""


def main():
    print("=" * 70)
    print("  PRACTICAL 1 & 2: METAMASK WALLET SETUP & ETHER TRANSACTIONS")
    print("=" * 70)

    # ── PART 1: Installation of MetaMask ────────────────────────────────
    print(f"\n{'─' * 70}")
    print("  PART 1: INSTALLATION OF METAMASK")
    print(f"{'─' * 70}")

    steps_install = [
        "1. Open Google Chrome (or Firefox/Brave).",
        "2. Go to https://metamask.io/download/",
        "3. Click 'Install MetaMask for Chrome' → 'Add to Chrome' → 'Add Extension'.",
        "4. MetaMask fox icon appears in the browser toolbar.",
        "5. Click the icon → 'Get Started'.",
    ]
    print("\n  Steps to Install MetaMask:")
    for step in steps_install:
        print(f"    {step}")

    # ── PART 2: Create Your Own Wallet ──────────────────────────────────
    print(f"\n{'─' * 70}")
    print("  PART 2: CREATING YOUR OWN WALLET")
    print(f"{'─' * 70}")

    steps_wallet = [
        "1. Click 'Create a Wallet'.",
        "2. Set a strong password (minimum 8 characters).",
        "3. IMPORTANT: Write down the 12-word Secret Recovery Phrase on paper.",
        "   (This is the ONLY way to recover your wallet if you lose access.)",
        "4. Confirm the recovery phrase by selecting the words in correct order.",
        "5. Your wallet is now created!",
        "",
        "   Your wallet address looks like: 0xAbC123...dEf456",
        "   This is your public address — safe to share for receiving crypto.",
    ]
    print("\n  Steps to Create Wallet:")
    for step in steps_wallet:
        print(f"    {step}")

    # ── PART 3: Connect to a Test Network ───────────────────────────────
    print(f"\n{'─' * 70}")
    print("  PART 3: CONNECT TO A TEST NETWORK (Sepolia)")
    print(f"{'─' * 70}")

    steps_testnet = [
        "1. In MetaMask, click the network dropdown (top, says 'Ethereum Mainnet').",
        "2. Click 'Show/hide test networks' → Enable test networks.",
        "3. Select 'Sepolia Test Network'.",
        "4. Get free test Ether from a faucet:",
        "   → https://sepoliafaucet.com/  OR",
        "   → https://www.alchemy.com/faucets/ethereum-sepolia",
        "5. Paste your wallet address → Request test ETH.",
        "6. Wait ~30 seconds. Test ETH will appear in your MetaMask wallet.",
    ]
    print("\n  Steps:")
    for step in steps_testnet:
        print(f"    {step}")

    # ── PART 4: Sending a Transaction & Studying Gas Fees ───────────────
    print(f"\n{'─' * 70}")
    print("  PART 4: SENDING ETHER & STUDYING TRANSACTION FEES")
    print(f"{'─' * 70}")

    steps_tx = [
        "1. In MetaMask, click 'Send'.",
        "2. Enter a recipient address (another wallet or your second account).",
        "3. Enter amount (e.g., 0.01 ETH).",
        "4. MetaMask shows the estimated Gas Fee before confirming.",
        "",
        "   TRANSACTION FEE BREAKDOWN:",
        "   ─────────────────────────────────────────────",
        "   • Gas Limit   : Max units of gas for the transaction (e.g., 21,000)",
        "   • Gas Price    : Cost per unit of gas in Gwei (e.g., 20 Gwei)",
        "   • Total Fee    : Gas Limit × Gas Price",
        "   • Example      : 21,000 × 20 Gwei = 420,000 Gwei = 0.00042 ETH",
        "   ─────────────────────────────────────────────",
        "",
        "5. Click 'Confirm' to send the transaction.",
        "6. View transaction on Etherscan: https://sepolia.etherscan.io/",
        "   Enter your transaction hash to see full details:",
        "   → Status, Block Number, Gas Used, Transaction Fee, etc.",
    ]
    print("\n  Steps:")
    for step in steps_tx:
        print(f"    {step}")

    # ── Key Observations ────────────────────────────────────────────────
    print(f"\n{'═' * 70}")
    print("  KEY OBSERVATIONS")
    print(f"{'═' * 70}")

    observations = [
        "1. Simple ETH transfers use exactly 21,000 gas units.",
        "2. Smart contract interactions use more gas (varies by complexity).",
        "3. Gas price fluctuates based on network congestion.",
        "4. Transaction Fee = Gas Used × Gas Price (in Gwei).",
        "5. 1 Gwei = 0.000000001 ETH (10^-9 ETH).",
        "6. MetaMask shows estimated fee before confirming any transaction.",
        "7. Failed transactions still consume gas (the fee is not refunded).",
        "8. Test networks (Sepolia) use fake ETH with no real monetary value.",
    ]
    print()
    for obs in observations:
        print(f"    {obs}")

    print(f"\n{'═' * 70}")
    print("  CONCLUSION")
    print(f"{'═' * 70}")
    print("""
    MetaMask is a browser-based Ethereum wallet that allows users to:
      • Store and manage ETH and ERC-20 tokens
      • Interact with decentralized applications (dApps)
      • Send and receive cryptocurrency
      • Connect to test networks for development

    Each transaction on Ethereum requires a gas fee, which compensates
    miners/validators for processing the transaction. The fee depends
    on the complexity of the transaction and current network congestion.
    """)
    print(f"{'═' * 70}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  PRACTICAL 1 & 2: METAMASK WALLET SETUP & ETHER TRANSACTIONS

  PART 1: INSTALLATION OF METAMASK
    1. Open Google Chrome (or Firefox/Brave).
    2. Go to https://metamask.io/download/
    3. Click 'Install MetaMask for Chrome' → 'Add to Chrome'.
    ...

  PART 2: CREATING YOUR OWN WALLET
    1. Click 'Create a Wallet'.
    2. Set a strong password.
    3. Write down the 12-word Secret Recovery Phrase.
    ...

  PART 4: SENDING ETHER & STUDYING TRANSACTION FEES
    Gas Limit: 21,000 | Gas Price: 20 Gwei | Total: 0.00042 ETH

  KEY OBSERVATIONS
    1. Simple ETH transfers use exactly 21,000 gas units.
    2. Gas price fluctuates based on network congestion.
    ...

========================================================================
"""
