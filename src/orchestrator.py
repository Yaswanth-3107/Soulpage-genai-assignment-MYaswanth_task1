from typing import Optional
from uuid import uuid4
from .graph import build_graph
from .utils import MarketSummary

def run_market_summary(company: str, ticker: str, session_id: Optional[str] = None) -> MarketSummary:
    """
    Orchestrates the LangGraph flow and returns a MarketSummary.
    session_id -> used as LangGraph checkpointer thread_id. If None, a UUID is used.
    """
    app = build_graph()
    thread_id = session_id or f"market-{ticker}-{uuid4()}"

    initial_state = {
        "company": company,
        "ticker": ticker,
        "collected": {},
        "analysis": {},
        "messages": [],
    }

    # IMPORTANT: provide configurable.thread_id for MemorySaver checkpointer
    final = app.invoke(
        initial_state,
        config={"configurable": {"thread_id": thread_id}},
    )

    collected = final["collected"]
    analysis_text = final["analysis"]["analysis_text"]

    risks = []
    recs = []
    for line in analysis_text.splitlines():
        l = line.strip("-• ").strip()
        if not l:
            continue
        if l.lower().startswith(("risk:", "risk ")):
            risks.append(l.split(":", 1)[-1].strip())
        elif "risk" in l.lower() and len(l.split()) <= 25:
            risks.append(l)
        elif l.lower().startswith(("recommendation:", "buy", "hold", "sell")) or "recommend" in l.lower():
            recs.append(l)

    summary = MarketSummary(
        company=company,
        price_snapshot=collected.get("stock", {}),
        top_news=collected.get("news", [])[:5],
        analysis=analysis_text,
        risks=risks[:6],
        recommendations=recs[:5],
    )
    return summary
