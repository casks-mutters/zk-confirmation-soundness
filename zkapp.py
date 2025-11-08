# app.py
import os
import sys
import json
import time
import argparse
from datetime import datetime
from web3 import Web3
from web3.exceptions import TransactionNotFound

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def get_block_diff(w3: Web3, tx_hash: str) -> dict:
    """
    Measure how many blocks passed between the transaction submission and inclusion.
    """
    try:
        tx = w3.eth.get_transaction(tx_hash)
    except TransactionNotFound:
        raise RuntimeError("Transaction not found — it might still be pending.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch transaction: {e}")

    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
    except TransactionNotFound:
        raise RuntimeError("Transaction receipt not available yet.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch transaction receipt: {e}")

    submit_block = tx.blockNumber
    confirm_block = receipt.blockNumber
    if submit_block is None or confirm_block is None:
        raise RuntimeError("Incomplete transaction data — still pending?")

    diff = confirm_block - submit_block
    return {
        "submit_block": submit_block,
        "confirm_block": confirm_block,
        "block_diff": diff,
        "status": "✅ Success" if receipt.status == 1 else "❌ Failed",
    }

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-confirmation-soundness — verify transaction confirmation distance (in blocks) and analyze RPC inclusion soundness."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--tx", required=True, help="Transaction hash to analyze")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout in seconds (default: 30)")
    p.add_argument("--json", action="store_true", help="Output results in JSON format")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    start = time.time()

    if not args.rpc.startswith("http"):
        print("❌ Invalid RPC URL format. It must start with 'http' or 'https'.")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check RPC_URL or --rpc argument.")
        sys.exit(1)

    print(f"🕒 Timestamp: {datetime.utcnow().isoformat()}Z")
    print("🔧 zk-confirmation-soundness")
    print(f"🔗 RPC: {args.rpc}")
    print(f"🔍 Transaction: {args.tx}")

    # ✅ Validate transaction hash format
    if not args.tx.startswith("0x") or len(args.tx) != 66:
        print("❌ Invalid transaction hash format. Must be a 0x-prefixed 66-character string.")
        sys.exit(1)

    try:
        data = get_block_diff(w3, args.tx)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(2)

    print(f"🧱 Submission Block: {data['submit_block']}")
    print(f"🏗️  Confirmation Block: {data['confirm_block']}")
    print(f"📏 Block Difference: {data['block_diff']}")
    print(f"📦 Status: {data['status']}")

    # ✅ Add confirmation time (in seconds)
    try:
        block_time = w3.eth.get_block(data['confirm_block']).timestamp - w3.eth.get_block(data['submit_block']).timestamp
        print(f"⏱️ Confirmation Time: {block_time}s")
    except Exception:
        print("⚠️ Could not compute confirmation time (missing timestamp data).")

    if data["block_diff"] == 0:
        print("⚡ Transaction included in the same block — extremely fast inclusion!")
    elif data["block_diff"] > 100:
        print("🐢 Slow confirmation — network congestion or pending pool delays detected.")

    elapsed = time.time() - start
    print(f"✅ Completed in {elapsed:.2f}s")

    if args.json:
        result = {
            "rpc": args.rpc,
            "transaction": args.tx,
            "submit_block": data["submit_block"],
            "confirm_block": data["confirm_block"],
            "block_diff": data["block_diff"],
            "status": data["status"],
            "elapsed_seconds": round(elapsed, 2),
            "timestamp_utc": datetime.utcnow().isoformat() + "Z"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0)

if __name__ == "__main__":
    main()
