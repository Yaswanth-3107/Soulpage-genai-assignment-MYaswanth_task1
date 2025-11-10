import argparse
from uuid import uuid4
from src.orchestrator import run_market_summary
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True, help="Company name, e.g., Apple Inc.")
    parser.add_argument("--ticker", required=True, help="Ticker symbol, e.g., AAPL")
    parser.add_argument("--session-id", default=None, help="Optional thread_id for LangGraph checkpointer")
    args = parser.parse_args()

    session_id = args.session_id or f"cli-{args.ticker}-{uuid4()}"
    result = run_market_summary(args.company, args.ticker, session_id=session_id)
    print(json.dumps(result.model_dump(), indent=2))

if __name__ == "__main__":
    main()
