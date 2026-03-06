import sys
import pysqlite3

sys.modules["sqlite3"] = pysqlite3

import uuid
from my_agent.app import app
from my_agent.nodes import SYSTEM_PROMPT
from langchain_core.messages import SystemMessage


def run_interactive_agent():
    thread_id = "sessione_1"
    config = {"configurable": {"thread_id": thread_id}}

    print(f"\033[94m--- AGENTE CON MEMORIA ATTIVA (ID: {thread_id}) ---\033[0m")

    # "Warm-up": Inizializziamo il thread solo se è vuoto
    # Recuperiamo lo stato attuale per vedere se esiste
    state = app.get_state(config)
    if not state.values or "messages" not in state.values:
        print("\033[90mInizializzazione contesto di sistema...\033[0m")
        app.update_state(config, {"messages": [SystemMessage(content=SYSTEM_PROMPT)]})

    while True:
        user_input = input("\033[92mTu:\033[0m ").strip()
        if user_input.lower() in ['exit', 'quit']: break

        input_data = {"messages": [("user", user_input)]}

        try:
            for event in app.stream(input_data, config, stream_mode="values"):
                if "messages" in event:
                    msg = event["messages"][-1]

                    # VERIFICA SICURA: controlla se il messaggio è dell'AI
                    if msg.type == "ai":
                        # Ora puoi controllare i tool in sicurezza
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            print(f"\033[93m[EXEC]: {msg.tool_calls[0]['name']}\033[0m")
                        # Stampa il contenuto testuale solo se c'è e se non è un messaggio di sistema
                        elif msg.content:
                            print(f"\n\033[96mAI:\033[0m {msg.content}\n")
        except Exception as e:
            print(f"\033[91m[ERRORE]: {e}\033[0m")


if __name__ == "__main__":
    run_interactive_agent()