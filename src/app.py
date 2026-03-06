import sqlite3
import os
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes import call_model, call_tools, summarize_history

# Setup directory
base_dir = Path(__file__).parent.parent
data_dir = base_dir / "data"
os.makedirs(data_dir, exist_ok=True)
db_path = data_dir / "checkpoints.db"

# Setup Persistenza
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)


def router(state):
    """Router unico: decide il prossimo passo basandosi sullo stato."""
    messages = state["messages"]
    last_message = messages[-1]

    # 1. Priorità: Memoria (se > 15 messaggi)
    if len(messages) > 5:
        return "summarize"

    # 2. Priorità: Azioni (se ci sono chiamate a tool)
    if last_message.tool_calls:
        return "action"

    # 3. Stop
    return END


def create_app():
    def initialize_state(messages):
        return {"messages": [SystemMessage(content=SYSTEM_PROMPT)] + messages}

    workflow = StateGraph(AgentState)

    # Nodi
    workflow.add_node("agent", call_model)
    workflow.add_node("action", call_tools)
    workflow.add_node("summarize", summarize_history)

    # Entry point
    workflow.set_entry_point("agent")

    # Routing unico dopo ogni interazione con l'agente
    workflow.add_conditional_edges(
        "agent",
        router,
        {
            "summarize": "summarize",
            "action": "action",
            "__end__": END
        }
    )

    # Ritorno al nodo agente dopo ogni operazione
    workflow.add_edge("action", "agent")
    workflow.add_edge("summarize", "agent")

    return workflow.compile(checkpointer=memory, debug=False)


app = create_app()