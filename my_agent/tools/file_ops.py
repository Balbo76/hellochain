import os
from pathlib import Path

# Definiamo la cartella del progetto come UNICA zona accessibile
# .parent.parent.parent ci porta fuori da my_agent/tools/ alla root del progetto
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()


def create_new_file(filename: str, content: str) -> str:
    """Crea un file solo dentro la cartella del progetto."""
    # .name assicura che non possa usare "../../etc/passwd"
    safe_path = PROJECT_ROOT / Path(filename).name

    with open(safe_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File '{safe_path.name}' creato in {PROJECT_ROOT.name}."


def list_files(directory: str = ".") -> str:
    """Elenca i file solo dentro la cartella del progetto."""
    # Impediamo di risalire l'albero con ".."
    safe_path = PROJECT_ROOT

    files = os.listdir(safe_path)
    # Filtriamo per non mostrare le cartelle nascoste o il venv se non vuoi
    visible_files = [f for f in files if not f.startswith('.') and f != 'venv']

    return f"File nel progetto '{PROJECT_ROOT.name}': " + ", ".join(visible_files)


def read_file(filename: str) -> str:
    """Legge un file solo se è dentro la cartella del progetto."""
    safe_path = PROJECT_ROOT / Path(filename).name

    if not safe_path.exists():
        return f"Errore: Il file '{safe_path.name}' non esiste nella cartella di lavoro."

    with open(safe_path, "r", encoding="utf-8") as f:
        content = f.read()
    return f"Contenuto di '{safe_path.name}':\n\n{content}"