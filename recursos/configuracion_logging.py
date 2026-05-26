from __future__ import annotations

import logging
from pathlib import Path


NOMBRE_LOGGER = "monitor_recursos"


def configurar_logging() -> logging.Logger:
    """Configura y devuelve el logger principal del proyecto.

    - Crea el directorio `logs` en la raíz del proyecto si no existe.
    - Añade un handler de archivo y uno de consola con formato legible en español.
    - Si el logger ya tiene handlers, no hace nada (evita duplicados).
    """
    logger = logging.getLogger(NOMBRE_LOGGER)
    if logger.handlers:
        return logger

    raiz_proyecto = Path(__file__).resolve().parents[1]
    directorio_logs = raiz_proyecto / "logs"
    directorio_logs.mkdir(parents=True, exist_ok=True)
    ruta_log = directorio_logs / "monitor_recursos.log"

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formato = logging.Formatter(
        "%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    manejador_archivo = logging.FileHandler(ruta_log, encoding="utf-8")
    manejador_archivo.setLevel(logging.INFO)
    manejador_archivo.setFormatter(formato)

    manejador_consola = logging.StreamHandler()
    manejador_consola.setLevel(logging.INFO)
    manejador_consola.setFormatter(formato)

    logger.addHandler(manejador_archivo)
    logger.addHandler(manejador_consola)

    logger.info("Logger inicializado. Archivo de log: %s", ruta_log)

    return logger
