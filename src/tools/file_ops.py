import os
import shutil
from pathlib import Path
from langchain_core.tools import tool
from src.utils.workspace import secure_path, WORKSPACE_DIR

PROJECT_ROOT = WORKSPACE_DIR.parent


@tool
def create_new_file(filename: str, content: str) -> str:
    """Crea un file esclusivamente dentro la cartella /workspace."""
    try:
        # Usiamo la TUA utility di sicurezza che abbiamo già validato
        safe_path = secure_path(filename)

        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{safe_path.name}' creato correttamente."
    except PermissionError as e:
        return f"Errore di sicurezza: {str(e)}"
    except Exception as e:
        return f"Errore critico durante la scrittura: {str(e)}"


@tool
def list_files() -> str:
    """Elenca tutti i file contenuti nella cartella /workspace."""
    try:
        files = os.listdir(WORKSPACE_DIR)
        return f"File presenti nella workspace: {', '.join(files) if files else 'Nessuno'}"
    except Exception as e:
        return f"Errore durante l'elenco dei file: {str(e)}"


@tool
def read_file(filename: str) -> str:
    """Legge un file solo se si trova dentro la cartella /workspace."""
    try:
        # Usiamo secure_path anche qui per bloccare tentativi di escape
        safe_path = secure_path(filename)

        if not safe_path.exists():
            return f"Errore: Il file '{safe_path.name}' non esiste."

        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"Contenuto di '{safe_path.name}':\n\n{content}"
    except PermissionError as e:
        return f"Errore di sicurezza: {str(e)}"
    except Exception as e:
        return f"Errore durante la lettura: {str(e)}"


@tool
def get_workspace_stats() -> str:
    """Restituisce un sommario dei file presenti, inclusi pesi e date di modifica."""
    stats = []
    for path in WORKSPACE_DIR.rglob("*"):
        if path.is_file():
            stats.append(f"{path.name} ({path.stat().st_size} bytes)")
    return "\n".join(stats) if stats else "Workspace vuoto."


@tool
def delete_file(filename: str) -> str:
    """Elimina un file in modo sicuro, spostandolo nel cestino interno."""
    target = secure_path(filename)
    trash_dir = WORKSPACE_DIR / ".trash"
    trash_dir.mkdir(exist_ok=True)

    if target.exists():
        shutil.move(str(target), str(trash_dir / target.name))
        return f"File {target.name} eliminato (spostato nel trash)."
    return "Errore: file non trovato."