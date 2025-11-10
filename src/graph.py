from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AnyMessage, AIMessage
from .agents import data_collector, analyst

class OrchestratorState(TypedDict):
    company: str
    ticker: str
    collected: Dict[str, Any]
    analysis: Dict[str, Any]
    messages: List[AnyMessage]

def _collect(state: OrchestratorState) -> OrchestratorState:
    payload = data_collector(state["company"], state["ticker"])
    state["collected"] = payload
    state["messages"].append(AIMessage(content=f"Collected data for {state['company']} ({state['ticker']})."))
    return state

def _analyze(state: OrchestratorState) -> OrchestratorState:
    result = analyst(state["collected"])
    state["analysis"] = result
    state["messages"].append(AIMessage(content="Completed analysis."))
    return state

def build_graph():
    workflow = StateGraph(OrchestratorState)
    memory = MemorySaver()

    workflow.add_node("collect", _collect)
    workflow.add_node("analyze", _analyze)

    workflow.add_edge(START, "collect")
    workflow.add_edge("collect", "analyze")
    workflow.add_edge("analyze", END)

    app = workflow.compile(checkpointer=memory)
    return app
