import os
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    """Restituisce l'istanza dell'LLM configurata tramite variabili d'ambiente."""
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "google":
        print(f"\033[92m[CONFIG]: Inizializzazione Gemini 2.0 Flash\033[0m")
        return ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    else:
        print(f"\033[93m[CONFIG]: Inizializzazione Ollama (qwen2.5-coder:7b)\033[0m")
        return ChatOllama(model="qwen2.5-coder:7b")