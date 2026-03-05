import pysqlite3
import sys
sys.modules["sqlite3"] = pysqlite3 # Sostituisce la libreria di sistema con quella nuova

import uuid
from my_agent.app import app


def run_interactive_agent():

    thread_id = "sviluppatore_32core"
    config = {"configurable": {"thread_id": "sessione_1"}}

    print(f"\033[94m--- AGENTE CON MEMORIA ATTIVA (ID: {thread_id}) ---\033[0m")

    current_state = None

    while True:
        user_input = input("\033[92mTu:\033[0m ").strip()
        if user_input.lower() in ['exit', 'quit']: break

        input_data = {"messages": [("user", user_input)]}

        try:
            # Il grafo ora sa chi sei grazie a config
            for event in app.stream(input_data, config, stream_mode="values"):
                if "messages" in event:
                    last_msg = event["messages"][-1]
                    if last_msg.type == "ai" and last_msg.content:
                        print(f"\n\033[96mAI:\033[0m {last_msg.content}\n")
        except Exception as e:
            print(f"\033[91m[ERRORE]: {e}\033[0m")


if __name__ == "__main__":
    run_interactive_agent()