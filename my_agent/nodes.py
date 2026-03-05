from langgraph.prebuilt import ToolNode
from my_agent.tools import all_tools
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

print("\033[94m[DEBUG] nodes.py: Caricamento tool e Qwen 2.5\033[0m")

model = ChatOllama(model="qwen2.5:7b", temperature=0).bind_tools(all_tools)
summarizer_llm = ChatOllama(model="qwen2.5:7b", temperature=0)
call_tools = ToolNode(all_tools)

def call_model(state):
    print(f"\n[BRAIN] L'agente sta pensando... (Messaggi nel contesto: {len(state['messages'])})")
    # Usa il modello globale definito sopra
    response = model.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    print(f"\n[ACTION] L'agente ha deciso di usare un tool: {last_message.tool_calls[0]['name']}!")
    return "continue"


def should_summarize(state):
    # Logica di controllo per il grafo
    if len(state["messages"]) > 10:
        print(f"\n[MEMORY] Soglia superata ({len(state['messages'])} messaggi). Innesco riassunto...")
        return "summarize"
    return "agent"


def summarize_history(state):
    messages = state["messages"]
    print(f"✂️ [SUMMARIZE] Tentativo di compressione su {len(messages)} messaggi...")

    existing_summary = state.get("summary", "")
    if existing_summary:
        summary_prompt = (
            f"Questo è il riassunto precedente: {existing_summary}\n\n"
            "Aggiornalo includendo le nuove informazioni dell'ultima parte della conversazione, "
            "mantenendo i dettagli tecnici e i file creati."
        )
    else:
        summary_prompt = "Riassumi la conversazione in modo conciso..."

    # Generiamo il riassunto (escludendo gli ultimi 2 messaggi per sicurezza)
    summary_response = summarizer_llm.invoke(messages[:-2] + [HumanMessage(content=summary_prompt)])
    new_summary = SystemMessage(content=f"Riassunto precedente: {summary_response.content}")

    # CREIAMO LE ISTRUZIONI DI CANCELLAZIONE
    # Diciamo a LangGraph di eliminare tutti i messaggi vecchi tranne gli ultimi 2
    delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2] if m.id is not None]

    # Restituiamo il riassunto + i messaggi di cancellazione + gli ultimi 2
    # LangGraph vedrà i RemoveMessage e pulirà il DB
    return {
        "messages": delete_messages + [new_summary] + messages[-2:]
    }