from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QSizePolicy, QGraphicsDropShadowEffect, QVBoxLayout, QLabel

class TarjetaInformativa(QFrame):
    def __init__(self, titulo: str, padre=None) -> None:
        super().__init__(padre)
        self.setObjectName("TarjetaInformativa")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(20)
        sombra.setOffset(0, 4)
        sombra.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(sombra)

        self.etiqueta_titulo = QLabel(titulo)
        self.etiqueta_titulo.setObjectName("TarjetaTitulo")

        self.etiqueta_valor = QLabel("--")
        self.etiqueta_valor.setObjectName("TarjetaValorTexto")
        self.etiqueta_valor.setWordWrap(True)

        self.etiqueta_detalle = QLabel("")
        self.etiqueta_detalle.setObjectName("TarjetaDetalle")
        self.etiqueta_detalle.setWordWrap(True)
        self.etiqueta_detalle.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        contenido = QVBoxLayout(self)
        contenido.setContentsMargins(18, 16, 18, 16)
        contenido.setSpacing(10)

        contenido.addWidget(self.etiqueta_titulo)
        contenido.addWidget(self.etiqueta_valor)
        contenido.addWidget(self.etiqueta_detalle, 1)

    def actualizar(self, valor: str, detalle: str = "", tono: str = "#e5e7eb") -> None:
        self.etiqueta_valor.setText(valor)
        self.etiqueta_valor.setStyleSheet(f"color: {tono};")
        self.etiqueta_detalle.setText(detalle)