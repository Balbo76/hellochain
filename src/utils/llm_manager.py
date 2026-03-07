import os
import re
from typing import List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, BaseMessage


def get_model():
    """Factory: Inizializza il modello in base alla variabile LLM_PROVIDER."""
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "google":
        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_MODEL_NAME", "gemini-3-flash-preview"),
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    else:
        # Default su Ollama (es. qwen2.5-coder)
        return ChatOllama(model=os.getenv("OLLAMA_MODEL_NAME", "qwen2.5-coder:7b"))


class LLMWrapper:
    """Proxy che avvolge il modello per pulire gli output automaticamente."""

    def __init__(self, model: Any):
        self.model = model

    def invoke(self, messages: List[BaseMessage], **kwargs: Any) -> AIMessage:
        """Metodo standard LangChain: delega al modello e pulisce l'output."""
        try:
            # Invoca il modello reale (Gemini o Ollama)
            raw_response = self.model.invoke(messages, **kwargs)
            # Applica il filtro di pulizia
            return self._normalize_response(raw_response)
        except Exception as e:
            print(f"[LLM_WRAPPER_ERROR] Fallimento invocazione: {e}")
            return AIMessage(content=f"Errore critico del modello: {str(e)}")

    def _normalize_response(self, response: AIMessage) -> AIMessage:
        """Logica di pulizia agnostica del provider."""
        content = response.content

        # 1. Normalizzazione se il contenuto è una lista (tipico di Gemini/API complesse)
        if isinstance(content, list):
            content = " ".join([item.get('text', '') for item in content if isinstance(item, dict)])

        # 2. Pulizia regex: rimuove metadati di Google (SynthID, extras, signature)
        # Questa regex rimuove blocchi come 'extras: { ... }' e tag di firma
        content = re.sub(r'(?i)(extras|signature|metadata):\s*\{.*?\}', '', content, flags=re.DOTALL)

        # Ritorna un oggetto pulito
        return AIMessage(content=content.strip())