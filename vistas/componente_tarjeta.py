from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QLabel, QProgressBar, QVBoxLayout

class TarjetaRecurso(QFrame):
    def __init__(self, titulo: str, unidad: str, padre=None) -> None:
        super().__init__(padre)
        self.setObjectName("TarjetaRecurso")

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(20)
        sombra.setOffset(0, 4)
        sombra.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(sombra)

        self.etiqueta_titulo = QLabel(titulo)
        self.etiqueta_titulo.setObjectName("TarjetaTitulo")

        self.etiqueta_detalle = QLabel(unidad)
        self.etiqueta_detalle.setObjectName("TarjetaDetalle")

        self.etiqueta_valor = QLabel("0%")
        self.etiqueta_valor.setObjectName("TarjetaValor")

        self.barra_progreso = QProgressBar()
        self.barra_progreso.setRange(0, 100)
        self.barra_progreso.setValue(0)
        self.barra_progreso.setTextVisible(False)

        contenido = QVBoxLayout(self)
        contenido.setContentsMargins(18, 16, 18, 16)
        contenido.setSpacing(10)

        contenido.addWidget(self.etiqueta_titulo)
        contenido.addWidget(self.etiqueta_detalle)
        contenido.addWidget(self.etiqueta_valor)
        contenido.addWidget(self.barra_progreso)

    def actualizar(self, valor_porcentaje: float, detalle: str) -> None:
        valor_limite = max(0, min(100, int(round(valor_porcentaje))))
        self.etiqueta_valor.setText(f"{valor_porcentaje:.1f}%")
        self.etiqueta_detalle.setText(detalle)
        self.barra_progreso.setValue(valor_limite)
        self._aplicar_color(valor_limite)

    def _aplicar_color(self, valor_porcentaje: int) -> None:
        if valor_porcentaje >= 80:
            color = "#f87171"
        elif valor_porcentaje >= 60:
            color = "#fbbf24"
        else:
            color = "#34d399"

        self.barra_progreso.setStyleSheet(
            "QProgressBar {"
            " background-color: #1f2937;"
            " border: 1px solid #374151;"
            " border-radius: 6px;"
            " height: 10px;"
            " }"
            "QProgressBar::chunk {"
            f" background-color: {color};"
            " border-radius: 6px;"
            " }"
        )
