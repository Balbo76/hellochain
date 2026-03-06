import os
from langgraph.prebuilt import ToolNode
from my_agent.tools import all_tools
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from my_agent.utils.logger import setup_logger, get_resource_log

from my_agent.utils.workspace import secure_path, WORKSPACE_DIR
PROJECT_ROOT = WORKSPACE_DIR.parent


log = setup_logger("AGENT")

model = ChatOllama(model="qwen2.5:7b", temperature=0).bind_tools(all_tools)
summarizer_llm = ChatOllama(model="qwen2.5:7b", temperature=0)

call_tools = ToolNode(all_tools)

SYSTEM_PROMPT = """Sei un Architetto Software Senior e un esperto di automazione file-system.
Operi esclusivamente all'interno della cartella '/workspace'. 

REGOLAMENTO OPERATIVO (RIGOROSO):
1. MODALITÀ EXEC: Non fornire mai feedback testuale intermedi (es. "Sto creando il file...", "Ho finito il passaggio 1..."). Ogni tuo output testuale deve essere o una chiamata a un tool, o la risposta finale conclusiva.
2. ATOMICITÀ: Se ti viene assegnato un task complesso, scomponilo internamente e rispondi concatenando le chiamate ai tool. Esegui le azioni in silenzio.
3. OUTPUT: Se un tool restituisce un output, non ripetere il contenuto dell'output nell'AI Message. Analizzalo e passa allo step successivo.
4. PERSONALITÀ: Sei sintetico, tecnico, preciso. Non sei un assistente chiacchierone, sei un'interfaccia di esecuzione.
5. SICUREZZA: Ogni operazione di scrittura/lettura deve essere validata tramite la funzione `secure_path`. Non tentare MAI di accedere a percorsi esterni alla /workspace.

Se ti chiedo un task, il risultato deve essere il completamento dell'azione, non un saggio sulla stessa.
"""


def call_model(state):
    log.info(f"Avvio inferenza LLM. Contesto: {len(state['messages'])} messaggi")

    # Invia lo stato attuale (che dovrebbe già contenere il SystemMessage all'indice 0)
    response = model.invoke(state["messages"])

    # Log del risultato per debug immediato
    if response.tool_calls:
        log.info(f"✅ Tool chiamati: {response.tool_calls}")
    else:
        log.info("ℹ️ Risposta testuale (nessun tool chiamato).")

    return {"messages": [response]}


def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    log.info(f"\n[ACTION] L'agente ha deciso di usare un tool: {last_message.tool_calls[0]['name']}!")
    return "continue"


def should_summarize(state):
    if len(state["messages"]) > 5:
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