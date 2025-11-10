from typing import List, Dict, Any, Optional
import yfinance as yf
from duckduckgo_search import DDGS
import wikipedia

def fetch_stock_snapshot(ticker: str) -> Dict[str, Any]:
    """
    Robust snapshot with yfinance that avoids FastInfo.get() KeyError and handles rate-limits.
    - Prefer fast_info via getattr (no .get()).
    - Fall back to t.info when needed.
    - Never throw on missing fields (return None instead).
    """
    t = yf.Ticker(ticker)

    # --- price history (safe) ---
    last_close: Optional[float] = None
    change_pct_5d: Optional[float] = None
    try:
        hist = t.history(period="5d")
        if not hist.empty:
            last_close = float(hist["Close"].iloc[-1])
            if len(hist["Close"]) >= 2:
                prev = float(hist["Close"].iloc[0])
                if prev:
                    change_pct_5d = round((last_close - prev) / prev * 100, 2)
    except Exception:
        # yfinance rate limit or no data — leave as None
        pass

    # --- fast_info (avoid .get) ---
    currency = None
    exchange = None
    try:
        fi = getattr(t, "fast_info", None)
        if fi is not None:
            currency = getattr(fi, "currency", None)
            exchange = getattr(fi, "exchange", None) or getattr(fi, "market", None)
    except Exception:
        pass

    # --- fall back to .info only if needed (slower / may 429) ---
    market_cap = None
    try:
        info = getattr(t, "info", {}) or {}
        if currency is None:
            currency = info.get("currency")
        if exchange is None:
            exchange = info.get("exchange") or info.get("market")
        market_cap = info.get("marketCap")
    except Exception:
        pass

    return {
        "ticker": ticker,
        "currency": currency,          # may be None if unavailable
        "exchange": exchange,          # may be None if unavailable
        "last_close": last_close,
        "five_day_change_pct": change_pct_5d,
        "market_cap": market_cap,
    }

def fetch_company_news_ddg(company: str, limit: int = 8) -> List[Dict[str, Any]]:
    """
    DuckDuckGo news (free). Handles rate-limit by returning empty list instead of raising.
    """
    out: List[Dict[str, Any]] = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.news(keywords=company, max_results=limit, safesearch="moderate"):
                out.append({
                    "title": item.get("title"),
                    "source": item.get("source"),
                    "date": item.get("date"),
                    "url": item.get("url"),
                    "snippet": item.get("excerpt"),
                })
    except Exception:
        # Rate-limited or network error — return no news
        return []
    return out

def wiki_summary(query: str, sentences: int = 3) -> str:
    try:
        wikipedia.set_lang("en")
        page = wikipedia.page(query, auto_suggest=True, redirect=True)
        return wikipedia.summary(page.title, sentences=sentences)
    except Exception:
        try:
            return wikipedia.summary(query, sentences=sentences)
        except Exception:
            return "No Wikipedia summary available."
