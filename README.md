# Company Intelligence Multi-Agent System (LangGraph + GROQ + Streamlit)

This project implements **Task 1** of the assignment:  
✅ A **multi‑agent system** using **LangGraph**  
✅ Powered by **GROQ LLMs**  
✅ Fully interactive **Streamlit dashboard**  
❌ Knowledge Bot removed (as requested)  
✅ Robust API handling (Yahoo Finance & DuckDuckGo rate-limit safe)

---

## Architecture

<p align="center"> <img src="https://github.com/Yaswanth-3107/Soulpage-genai-assignment-MYaswanth_task1/blob/main/architecture.png" width="80%" /> </p>



## ✅ Features

### ✅ Two-Agent Architecture
1. **Agent 1 — Data Collector**
   - Fetches:
     - Stock price snapshot (via yfinance)
     - Company news (DuckDuckGo)
     - Background summary (Wikipedia)
   - Hardened for:
     - Yahoo 429 rate limits
     - Missing ticker data

2. **Agent 2 — Analyst**
   - Uses GROQ LLM (`llama-3.1-8b-instant`)
   - Generates:
     - Risk factors
     - Actionable recommendations
     - Narrative summary

---

## ✅ Tech Stack

| Component | Tech |
|----------|------|
| LLM Backend | GROQ |
| Multi-agent engine | LangGraph |
| Orchestration | StateGraph + MemorySaver |
| Front-end UI | Streamlit |
| Stocks | yfinance (Yahoo) |
| News | DuckDuckGo Search |
| Background | Wikipedia API |

---

## ✅ Project Structure

```
project/
│
├── streamlit_app.py         # Streamlit UI
├── main.py                  # CLI runner (optional)
│
└── src/
    ├── orchestrator.py      # Graph invoke wrapper
    ├── graph.py             # LangGraph state machine
    ├── agents.py            # DataCollector + Analyst agent code
    ├── tools.py             # Stock, news, and wiki utilities
    ├── config.py            # LLM backend selection
    ├── utils.py             # Data models
```

---

## ✅ Installation

### 1) Clone repo & create virtual env
```bash
git clone https://github.com/Yaswanth-3107/Soulpage-genai-assignment-MYaswanth_task1.git
cd project
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure environment
Copy example:
```
cp .env.example .env
```
Edit `.env`:
```
MODEL_BACKEND=groq
GROQ_API_KEY=your-key-here
GROQ_MODEL=llama-3.1-8b-instant
```

---

## ✅ Running the App (Streamlit UI)

```bash
streamlit run streamlit_app.py
```

The dashboard will open in your browser.

---

## ✅ Usage Instructions

### ✅ Enter any company + ticker
Examples:

| Company | Ticker |
|--------|--------|
| Apple Inc. | AAPL |
| Tata Elxsi | TATAELXSI.NS |
| Happiest Minds | HAPPSTMNDS.NS |
| Infosys | INFY.NS |

> For Indian stocks:  
> NSE tickers end with `.NS`  
> BSE tickers end with `.BO`
>
> <p align="center"> <img src="https://github.com/Yaswanth-3107/Soulpage-genai-assignment-MYaswanth_task1/blob/main/images/Screenshot%202025-11-10%20110028.png" width="80%" /> </p>

### ✅ Press **Run Analysis**

<p align="center"> <img src="https://github.com/Yaswanth-3107/Soulpage-genai-assignment-MYaswanth_task1/blob/main/images/Screenshot%202025-11-10%20110125.png" width="80%" /> </p>

- Change Company Name

<p align="center"> <img src="https://github.com/Yaswanth-3107/Soulpage-genai-assignment-MYaswanth_task1/blob/main/images/Screenshot%202025-11-10%20110238.png" width="80%" /> </p>

The multi-agent system produces:

- Price Snapshot  
- Top News  
- Analyst Narrative  
- Risk Factors  
- Recommendations  

Even if Yahoo Finance or DDG rate-limit, the app continues gracefully.

---

## ✅ Notes on API Limitations

### ✅ Yahoo Finance (yfinance)
- May show:
```
429 Too Many Requests
possibly delisted
no price data found
```
The UI handles this safely (shows `None` and proceeds).

### ✅ DuckDuckGo
- May rate-limit during heavy usage  
- System safely returns empty news list  
- Analysis still works

---

## ✅ What This Project Demonstrates

- Proper **2‑agent system architecture**
- Correct usage of **LangGraph** with memory (`MemorySaver`)
- Ability to integrate **external tools** for data collection
- End-to-end **Streamlit application**
- **Robust and production-friendly** error handling





---

## ✅ License
MIT License
