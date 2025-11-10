import streamlit as st
from uuid import uuid4

from src.orchestrator import run_market_summary

st.set_page_config(page_title="Company Intelligence (2-Agent)", page_icon="📈", layout="centered")

st.title("📈 Company Intelligence — 2-Agent Analysis (Collector + Analyst)")

# persistent thread_id for LangGraph MemorySaver
if "graph_thread_id" not in st.session_state:
    st.session_state.graph_thread_id = f"streamlit-{uuid4()}"

st.markdown(
    """
Use any company name + ticker (e.g., **Apple Inc. / AAPL**, or **Tata Elxsi / TATAELXSI.NS**).
For Indian stocks on NSE append **.NS** (BSE: **.BO**). If price/news APIs rate-limit, the app
will still generate analysis from whatever data was collected.
"""
)

with st.form("company_form", clear_on_submit=False):
    c1, c2 = st.columns([2, 1])
    with c1:
        company = st.text_input("Company", value="Apple Inc.")
    with c2:
        ticker = st.text_input("Ticker", value="AAPL")

    colx, coly = st.columns([1, 1])
    with colx:
        use_news = st.checkbox("Fetch recent news (DuckDuckGo)", value=True,
                               help="Uncheck if you hit rate limits; analysis still works.")
    with coly:
        show_raw = st.checkbox("Show raw collected JSON", value=False)

    submitted = st.form_submit_button("Run Analysis", type="primary")

if submitted:
    with st.spinner("Collecting data & running analysis…"):
        summary = run_market_summary(company, ticker, session_id=st.session_state.graph_thread_id)

    st.success(f"Done — as of {summary.as_of}")

    # ---- price snapshot block (safe defaults) ----
    ps = summary.price_snapshot or {}
    last_close = ps.get("last_close")
    currency = ps.get("currency") or ""
    five_day = ps.get("five_day_change_pct")

    price_line = f"**{ticker}** • Last Close: `{last_close if last_close is not None else '—'}` {currency}"
    change_line = f" | 5D Change: `{str(five_day) + '%' if five_day is not None else '—'}`"
    st.markdown(price_line + change_line)

    # ---- News (optional) ----
    if use_news:
        if summary.top_news:
            st.markdown("### Top News")
            for n in summary.top_news:
                title = n.get("title") or "Untitled"
                url = n.get("url") or "#"
                source = n.get("source") or ""
                st.markdown(f"- [{title}]({url}) — *{source}*")
        else:
            st.info("No news available (might be rate-limited or none found).")
    else:
        st.info("News fetching disabled. You can enable it above.")

    # ---- Analyst narrative ----
    st.markdown("### Analyst Narrative")
    st.write(summary.analysis or "No analysis text produced.")

    # ---- Risks & Recommendations (optional sections) ----
    if summary.risks:
        st.markdown("### Risks")
        for r in summary.risks:
            st.markdown(f"- {r}")

    if summary.recommendations:
        st.markdown("### Recommendations")
        for r in summary.recommendations:
            st.markdown(f"- {r}")

    # ---- Raw collected (for debugging) ----
    if show_raw:
        import json
        st.markdown("### Raw Collected Data (debug)")
        st.code(json.dumps({
            "price_snapshot": summary.price_snapshot,
            "top_news": summary.top_news,
        }, indent=2))
