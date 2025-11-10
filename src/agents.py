from typing import Dict, Any
from langchain.schema import SystemMessage, HumanMessage
from .config import get_llm
from .tools import fetch_stock_snapshot, fetch_company_news_ddg, wiki_summary

def data_collector(company: str, ticker: str) -> Dict[str, Any]:
    stock = fetch_stock_snapshot(ticker)
    news = fetch_company_news_ddg(company)
    wiki = wiki_summary(company, sentences=3)
    return {"company": company, "ticker": ticker, "stock": stock, "news": news, "wiki": wiki}

def analyst(collected: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""You are a senior equity analyst. Using the JSON below, write a concise analysis:
- 4-6 bullet risk factors (clear, specific)
- 3-5 bullet actionable recommendations for an investor
- A brief 1-paragraph narrative summary

JSON:
{collected}
"""
    model = get_llm()
    resp = model.invoke([SystemMessage(content="Be accurate, measured, and practical."),
                         HumanMessage(content=prompt)])
    return {"analysis_text": resp.content}
