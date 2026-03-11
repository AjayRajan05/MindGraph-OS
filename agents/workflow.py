from langgraph.graph import StateGraph
from typing import TypedDict

from agents.contradiction_agent import run_contradiction_scan
from agents.connection_agent import find_connections
from agents.staleness_agent import find_stale_concepts


class AgentState(TypedDict):

    new_chunk: str
    contradictions: list
    connections: list
    stale: list


def contradiction_node(state):

    results = run_contradiction_scan(state["new_chunk"])

    state["contradictions"] = results

    return state


def connection_node(state):

    conns = find_connections()

    state["connections"] = conns

    return state


def staleness_node(state):

    stale = find_stale_concepts()

    state["stale"] = stale

    return state


graph = StateGraph(AgentState)

graph.add_node("contradiction", contradiction_node)
graph.add_node("connection", connection_node)
graph.add_node("staleness", staleness_node)

graph.set_entry_point("contradiction")

graph.add_edge("contradiction", "connection")
graph.add_edge("connection", "staleness")

agent_workflow = graph.compile()