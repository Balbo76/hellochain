import os
import logging
import sys
import psutil
from pathlib import Path

# Definizioni colori ANSI per la console
COLORS = {
    "INFO": "\033[94m",  # Blu
    "WARNING": "\033[93m",  # Giallo
    "ERROR": "\033[91m",  # Rosso
    "DEBUG": "\033[90m",  # Grigio
}
RESET = "\033[0m"


class CustomFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, RESET)
        # Formato: [HH:MM:SS] [LIVELLO] [NOME] Messaggio
        log_fmt = f"{color}[%(asctime)s] [%(levelname)s] [%(name)s]{RESET} %(message)s"
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


def setup_logger(name):
    # Definisci il path della cartella logs alla root del progetto
    log_dir = Path(__file__).parent.parent.parent / "logs"
    os.makedirs(log_dir, exist_ok=True)  # Crea la cartella se non esiste

    print(log_dir)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # ... (console_handler come prima)

        # Percorso del file log dentro la cartella logs
        log_file = log_dir / "agent_v03.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
        logger.addHandler(file_handler)

    return logger


def get_resource_log():
    """Funzione helper per monitorare i tuoi 32 thread"""
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    return f" | 📊 CPU:{cpu}% RAM:{ram}%"