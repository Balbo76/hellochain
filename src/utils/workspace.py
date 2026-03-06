import os
from pathlib import Path

# Definiamo la cartella di lavoro
WORKSPACE_DIR = Path(__file__).parent.parent.parent / "workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)


def secure_path(user_path: str) -> Path:
    """Forza ogni percorso a essere dentro la cartella workspace."""
    # Rimuove eventuali tentativi di uscire dalla cartella (es. ../../)
    clean_path = os.path.normpath(user_path).lstrip("/")
    final_path = WORKSPACE_DIR / clean_path

    # Controllo di sicurezza finale
    if not str(final_path).startswith(str(WORKSPACE_DIR)):
        raise PermissionError("Tentativo di accesso fuori dalla workspace!")

    return final_path