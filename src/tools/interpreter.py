import sys
import io
from pathlib import Path

# Impediamo l'uso di os, subprocess, ecc.
BANNED_MODULES = ['os', 'subprocess', 'shutil', 'sys', 'socket', 'requests']


def execute_python(code: str) -> str:
    """Esegue codice Python in una sandbox sicura e restituisce l'output."""

    # Check di sicurezza preventivo sul testo del codice
    for banned in BANNED_MODULES:
        if f"import {banned}" in code or f"from {banned}" in code:
            return f"Errore di Sicurezza: L'import del modulo '{banned}' è vietato."

    # Catturiamo l'output (stdout)
    output_buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_buffer

    # Creiamo un ambiente isolato per le variabili
    local_vars = {}

    try:
        # Rimuoviamo le built-in pericolose dall'ambiente di esecuzione
        safe_builtins = __builtins__.copy()
        # Se __builtins__ è un modulo (dipende dalla versione di Python)
        if hasattr(safe_builtins, '__dict__'):
            safe_builtins = safe_builtins.__dict__.copy()

        dangerous_funcs = ['open', 'exit', 'quit', 'help', 'copyright', 'credits', 'license']
        for func in dangerous_funcs:
            safe_builtins.pop(func, None)

        # Esecuzione controllata
        exec(code, {"__builtins__": safe_builtins}, local_vars)

        result = output_buffer.getvalue()
        return result if result else "Codice eseguito con successo (nessun output)."

    except Exception as e:
        return f"Errore durante l'esecuzione: {str(e)}"

    finally:
        # Ripristiniamo sempre lo stdout originale
        sys.stdout = old_stdout