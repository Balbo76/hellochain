import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

def get_safe_path(filename: str) -> Path:
    """Valida il percorso per evitare path traversal (es. ../../)"""
    safe_filename = Path(filename).name
    return WORKSPACE_DIR / safe_filename

def create_new_file(filename: str, content: str) -> str:
    """Crea un file solo ed esclusivamente dentro la cartella /workspace."""
    safe_path = get_safe_path(filename)
    try:
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{safe_path.name}' creato correttamente in /{safe_path.relative_to(PROJECT_ROOT)}."
    except Exception as e:
        return f"Errore critico durante la scrittura: {str(e)}"

def list_files() -> str:
    """Elenca solo i file contenuti esclusivamente dentro la cartella /workspace."""
    files = os.listdir(WORKSPACE_DIR)
    return f"File presenti nella workspace: {', '.join(files) if files else 'Nessuno'}"


def read_file(filename: str) -> str:
    """Legge un file solo se è dentro la cartella del progetto."""
    safe_path = PROJECT_ROOT / Path(filename).name

    if not safe_path.exists():
        return f"Errore: Il file '{safe_path.name}' non esiste nella cartella di lavoro."

    with open(safe_path, "r", encoding="utf-8") as f:
        content = f.read()
    return f"Contenuto di '{safe_path.name}':\n\n{content}"

