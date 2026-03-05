# HelloChain Agent v0.1

Assistente AI autonomo basato su **LangGraph** e **Ollama**, ottimizzato per architetture **i7 (16 Core / 32 Thread)**.

## 🚀 Caratteristiche Principali
* **🧠 Brain**: Qwen 2.5 (7B) via Ollama.
* **🌐 Web**: Ricerca integrata tramite DuckDuckGo.
* **🛡️ Sandbox**: File System e Python REPL isolati.
* **⚙️ Performance**: Ottimizzato per 32 thread su Linux.

## 📂 Struttura del Progetto

```text
hellochain/
├── my_agent/
│   ├── tools/          # Strumenti dell'agente
│   │   ├── file_ops.py    # Lettura/Scrittura sicura
│   │   ├── interpreter.py # Sandbox Python (REPL)
│   │   ├── web.py         # Ricerca DuckDuckGo
│   │   └── git_ops.py     # Gestione repository
│   ├── nodes.py        # Logica decisionale
│   ├── app.py          # Grafo LangGraph
│   └── state.py        # Stato dell'agente
├── main.py             # Entry point
└── .gitignore          # Filtri repository
```

## 📦 Installazione e Setup
1. **Ambiente**: python3 -m venv venv
2. **Attivazione**: source venv/bin/activate
3. **Dipendenze**: pip install -r requirements.txt

---
*Sviluppato su Linux - Architettura i7 32-Thread.*