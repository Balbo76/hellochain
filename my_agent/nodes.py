from langgraph.prebuilt import ToolNode
from my_agent.tools import all_tools
from langchain_ollama import ChatOllama

print("\033[94m[DEBUG] nodes.py: Caricamento tool e Qwen 2.5\033[0m")

call_tools = ToolNode(all_tools)

def call_model(state):
    messages = state["messages"]
    # Qwen 2.5 7B è perfetto per gestire la lettura/scrittura codice
    llm = ChatOllama(model="qwen2.5:7b", temperature=0).bind_tools(all_tools)
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    return "continue"