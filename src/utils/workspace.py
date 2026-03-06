import os
from pathlib import Path

# Definiamo la cartella di lavoro
WORKSPACE_DIR = Path(__file__).parent.parent.parent / "workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)


def secure_path(filename: str) -> Path:
    # Trasforma in path assoluto e risolve i symlink (evita trucchetti con i link)
    target = (WORKSPACE_DIR / filename).resolve()

    # Check di sicurezza: il path deve iniziare con il percorso del workspace
    if not str(target).startswith(str(WORKSPACE_DIR.resolve())):
        raise PermissionError(f"Tentativo di accesso non autorizzato a: {filename}")

    # Impedisci l'accesso a file critici o nascosti
    if target.name.startswith(('.', '__')):
        raise PermissionError("Accesso a file di sistema non consentito.")

    return target