import os
from dotenv import load_dotenv

load_dotenv()

# App mode (currently not used programmatically, but documented)
APP_MODE = os.getenv("APP_MODE", "streamlit")

# Backend selection
MODEL_BACKEND = os.getenv("MODEL_BACKEND", "groq").lower()

# GROQ
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# OPENAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# OLLAMA
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

# Temperatures
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))

def get_llm():
    """Return a ChatModel based on MODEL_BACKEND env.
    Supports: groq | openai | ollama | auto
    """
    backend = MODEL_BACKEND
    if backend == "auto":
        # try groq -> openai -> ollama
        if GROQ_API_KEY:
            backend = "groq"
        elif OPENAI_API_KEY:
            backend = "openai"
        else:
            backend = "ollama"

    if backend == "groq":
        from langchain_groq import ChatGroq
        if not GROQ_API_KEY:
            raise RuntimeError("MODEL_BACKEND=groq but GROQ_API_KEY is empty in .env")
        return ChatGroq(model=GROQ_MODEL, temperature=LLM_TEMPERATURE)
    elif backend == "openai":
        from langchain_openai import ChatOpenAI
        if not OPENAI_API_KEY:
            raise RuntimeError("MODEL_BACKEND=openai but OPENAI_API_KEY is empty in .env")
        return ChatOpenAI(model=OPENAI_MODEL, temperature=LLM_TEMPERATURE)
    elif backend == "ollama":
        # local inference
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(model=OLLAMA_MODEL, temperature=LLM_TEMPERATURE)
    else:
        raise ValueError(f"Unknown MODEL_BACKEND: {MODEL_BACKEND}")
