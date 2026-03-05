import os
from pathlib import Path

# Definiamo la cartella del progetto come UNICA zona accessibile
# .parent.parent.parent ci porta fuori da my_agent/tools/ alla root del progetto
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()


def create_new_file(filename: str, content: str) -> str:
    """
    MOLTO IMPORTANTE: Usa questo tool ogni volta che l'utente chiede di creare,
    scrivere o generare un file (.py, .md, .txt).
    Non limitarti a scrivere il testo nella chat, DEVI chiamare questa funzione
    per salvare fisicamente il file sul disco.
    """
    try:
        # Forza la scrittura nella cartella corrente del progetto
        path = os.path.join(os.getcwd(), filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{filename}' creato con successo in {path}."
    except Exception as e:
        return f"Errore durante la creazione del file: {str(e)}"


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