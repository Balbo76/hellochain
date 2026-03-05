from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from my_agent.state import AgentState
from my_agent.nodes import call_model, call_tools, should_continue

print("\033[94m[DEBUG] app.py: Graffo compilato con MemorySaver\033[0m")

memory = MemorySaver()


def create_app():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("action", call_tools)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END
        }
    )
    workflow.add_edge("action", "agent")
    return workflow.compile(checkpointer=memory)


app = create_app()