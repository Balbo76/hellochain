# 🤖 HelloChain Agent v0.1

### 🚀 Overview
**HelloChain** è un assistente AI autonomo basato su **LangGraph** e **Ollama**. Progettato per girare interamente in locale, è ottimizzato per architetture **i7 (16 Core / 32 Thread)**.

---

### 🛠️ Core Features
| Feature | Description |
| :--- | :--- |
| **🧠 Brain** | Qwen 2.5 (7B) via Ollama |
| **🌐 Web** | Ricerca DuckDuckGo (No API Key) |
| **🛡️ Sandbox** | File System e REPL blindati |
| **💾 Memory** | Persistence via LangGraph Checkpointers |

---

### 📂 Progetto
* **`my_agent/tools/`**: Suite di strumenti (File, REPL, Web).
* **`my_agent/nodes.py`**: Logica decisionale e binding LLM.
* **`my_agent/app.py`**: Definizione del workflow (Grafo).
* **`main.py`**: Interfaccia utente.



---

### ⚙️ Setup Rapido
1. **Ambiente**: `python3 -m venv venv`
2. **Attivazione**: `source venv/bin/activate`
3. **Dipendenze**: `pip install -r requirements.txt`

---

### 🔒 Sicurezza & Privacy
L'agente opera in una **Sandbox**. Non può uscire dalla cartella di progetto e il REPL non ha accesso ai comandi di sistema (`os`, `subprocess`). **Zero dati inviati al cloud.**

---
*Sviluppato su Linux - Architettura 32-Thread.*
