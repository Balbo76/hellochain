from langgraph.prebuilt import ToolNode
from my_agent.tools import all_tools
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from my_agent.utils.logger import setup_logger, get_resource_log

print("\033[94m[DEBUG] nodes.py: Caricamento tool e Qwen 2.5\033[0m")

model = ChatOllama(model="qwen2.5:7b", temperature=0).bind_tools(all_tools)
summarizer_llm = ChatOllama(model="qwen2.5:7b", temperature=0)
call_tools = ToolNode(all_tools)
log = setup_logger("AGENT")


SYSTEM_PROMPT = """Sei un Architetto Software Senior. 
Hai accesso a file system protetto nella cartella /workspace.
NON rispondere che non puoi eseguire operazioni: i tool che hai a disposizione sono fatti apposta per essere usati.
Quando l'utente ti chiede di creare file o strutture, usa i tool forniti (create_new_file, etc.) invece di descriverli a parole."""


def call_model(state):
    # Assicurati che il SystemMessage sia sempre il primo messaggio
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    log.info(f"Avvio inferenza LLM. Contesto: {len(messages)} messaggi{get_resource_log()}")
    response = model.invoke(messages)
    log.debug("Risposta generata correttamente.")
    return {"messages": [response]}


def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    log.info(f"\n[ACTION] L'agente ha deciso di usare un tool: {last_message.tool_calls[0]['name']}!")
    return "continue"


def should_summarize(state):
    if len(state["messages"]) > 15:
        log.info(f"\n[MEMORY] Soglia superata ({len(state['messages'])} messaggi). Innesco riassunto...")
        return "summarize"
    return "agent"


def summarize_history(state):
    messages = state["messages"]

    log.info(f"✂️ [SUMMARIZE] Tentativo di compressione su {len(messages)} messaggi...")

    existing_summary = state.get("summary", "")
    if existing_summary:
        summary_prompt = (
            f"Questo è il riassunto precedente: {existing_summary}\n\n"
            "Aggiornalo includendo le nuove informazioni dell'ultima parte della conversazione, "
            "mantenendo i dettagli tecnici e i file creati."
        )
    else:
        summary_prompt = "Riassumi la conversazione in modo conciso..."

    summary_response = summarizer_llm.invoke(messages[:-2] + [HumanMessage(content=summary_prompt)])
    new_summary = SystemMessage(content=f"Riassunto precedente: {summary_response.content}")

    delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2] if m.id is not None]

    return {
        "messages": delete_messages + [new_summary] + messages[-2:]
    }