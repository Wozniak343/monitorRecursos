from __future__ import annotations
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

_RUTA_LOGO = Path(__file__).resolve().parent / "Logo.png"
_pixmap_original: QPixmap | None = None
_pixmaps_escalados: dict[tuple[int, int], QPixmap] = {}
_icono_aplicacion: QIcon | None = None

def obtener_logo(tamano: int) -> QPixmap:
    global _pixmap_original

    ancho = max(1, tamano)
    alto = max(1, tamano)
    clave = (ancho, alto)
    cacheado = _pixmaps_escalados.get(clave)
    if cacheado is not None:
        return cacheado

    if _pixmap_original is None:
        _pixmap_original = QPixmap(str(_RUTA_LOGO))

    if _pixmap_original.isNull():
        return QPixmap()

    escalado = _pixmap_original.scaled(
        ancho,
        alto,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    _pixmaps_escalados[clave] = escalado
    return escalado

def obtener_icono_aplicacion() -> QIcon:
    global _icono_aplicacion

    if _icono_aplicacion is not None:
        return _icono_aplicacion

    icono = QIcon(str(_RUTA_LOGO))
    if icono.isNull():
        _icono_aplicacion = QIcon()
        return _icono_aplicacion

    for tamano in (16, 20, 24, 32, 40, 48, 64, 128, 256):
        pixmap = obtener_logo(tamano)
        if not pixmap.isNull():
            icono.addPixmap(pixmap)

    _icono_aplicacion = icono
    return _icono_aplicacion