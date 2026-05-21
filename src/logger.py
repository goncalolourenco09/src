import logging
import os
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, f"football_manager_{datetime.now().strftime('%Y-%m-%d')}.log")


def configurar_logger():
    """
    Configura o sistema de logging com dois handlers:
      - StreamHandler: mostra logs WARNING+ no terminal
      - FileHandler:   guarda logs DEBUG+ num ficheiro em /logs/
    """

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger_raiz = logging.getLogger()
    logger_raiz.setLevel(logging.DEBUG)

    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Handler terminal (WARNING e acima) ---
    handler_terminal = logging.StreamHandler()
    handler_terminal.setLevel(logging.WARNING)
    handler_terminal.setFormatter(formato)

    # --- Handler ficheiro (DEBUG e acima) ---
    handler_ficheiro = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler_ficheiro.setLevel(logging.DEBUG)
    handler_ficheiro.setFormatter(formato)

    logger_raiz.addHandler(handler_terminal)
    logger_raiz.addHandler(handler_ficheiro)

    logging.getLogger(__name__).info("Logger configurado — ficheiro: %s", LOG_FILE)
