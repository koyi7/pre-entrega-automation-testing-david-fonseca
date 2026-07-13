"""Configuración de logging para la suite de pruebas."""
import logging
from datetime import datetime
from pathlib import Path

from utils.paths import REPORTS_DIR

LOGS_DIR = REPORTS_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

_LOGGER_CONFIGURED = False


def get_logger(name: str = "automation") -> logging.Logger:
    """Devuelve un logger con salida a consola y a archivo en reports/logs/."""
    global _LOGGER_CONFIGURED

    logger = logging.getLogger(name)
    if _LOGGER_CONFIGURED:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(
        LOGS_DIR / f"ejecucion_{stamp}.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    _LOGGER_CONFIGURED = True
    return logger
