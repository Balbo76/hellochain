import sqlite3
import os
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END
from my_agent.state import AgentState
from my_agent.nodes import call_model, call_tools, should_continue, should_summarize, summarize_history

print("\033[94m[DEBUG] app.py: Grafo in fase di compilazione con SqliteSaver\033[0m")

base_dir = Path(__file__).parent.parent
data_dir = base_dir / "data"
os.makedirs(data_dir, exist_ok=True) # Crea la cartella se non esiste
db_path = data_dir / "checkpoints.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

def create_app():
    workflow = StateGraph(AgentState)

    # 1. Aggiunta dei nodi
    workflow.add_node("agent", call_model)
    workflow.add_node("action", call_tools)
    workflow.add_node("summarize", summarize_history)

    # 2. Logica di Ingresso Condizionale (Summarize o Agent)
    # Rimuoviamo set_entry_point("agent") perché deve decidere should_summarize
    workflow.set_conditional_entry_point(
        should_summarize,
        {
            "summarize": "summarize",
            "agent": "agent",
        }
    )

    # 3. Flusso del Sommario
    workflow.add_edge("summarize", "agent")

    # 4. Ciclo di esecuzione standard (Agent -> Action -> Agent)
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END
        }
    )
    workflow.add_edge("action", "agent")

    # Compilazione con checkpointer e debug attivo
    return workflow.compile(checkpointer=memory, debug=False)

app = create_app()