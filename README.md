# zk-confirmation-soundness

## Overview
**zk-confirmation-soundness** is a CLI utility that measures how many **blocks** and **seconds** it took for a transaction to confirm on-chain.  
It’s designed for developers and researchers working with zk-rollups like **Aztec** or **Zama**, where **confirmation latency** and **inclusion soundness** are critical for proof timing and security validation.

## Features
- ⏱️ Measures block difference between transaction submission and confirmation  
- 🧱 Fetches submission and confirmation block numbers  
- ⚡ Calculates confirmation time in seconds  
- 📦 Reports transaction success/failure status  
- 🧮 Detects unusually slow confirmations (pending pool congestion)  
- 🧰 JSON output for monitoring and CI systems  
- 🌍 Works on all EVM-compatible networks  

## Installation
1. Requires Python 3.9+  
2. Install dependencies:
   pip install web3
3. Optionally set your RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Analyze confirmation distance:
   python app.py --tx 0xYourTransactionHash

With custom RPC:
   python app.py --rpc https://arb1.arbitrum.io/rpc --tx 0xYourTransactionHash

Emit JSON for dashboards:
   python app.py --tx 0xYourTransactionHash --json

## Example Output
🕒 Timestamp: 2025-11-08T14:31:22.507Z  
🔧 zk-confirmation-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🔍 Transaction: 0x123abc456def789...  
🧱 Submission Block: 21051000  
🏗️  Confirmation Block: 21051005  
📏 Block Difference: 5  
📦 Status: ✅ Success  
⏱️ Confirmation Time: 62s  
✅ Completed in 0.48s  

## Notes
- **Soundness Metric:** The tool measures transaction inclusion consistency between submission and confirmation.  
- **Fast Inclusion:** If the transaction is mined in the same block, it indicates extremely low network latency or a local miner.  
- **Slow Confirmations:** If block difference >100, it’s a signal of congestion, mempool delays, or insufficient gas.  
- **CI Integration:** The JSON mode fits perfectly for automated inclusion checks and zk-proof pipeline audits.  
- **EVM Compatibility:** Supports Ethereum, Polygon, Base, Arbitrum, Optimism, and all EVM-derived networks.  
- **ZK Relevance:** Proof builders rely on consistent confirmation delays for deterministic sequencing in zero-knowledge proofs.  
- **Best Practice:** Use archive or full nodes for reliable block timestamp data.  
- **Exit Codes:**  
  `0` → Success  
  `2` → Transaction or RPC error.  
