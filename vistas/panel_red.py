from __future__ import annotations
from collections import deque
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

class GraficaRed(QWidget):
    def __init__(self, padre=None) -> None:
        super().__init__(padre)
        self._valores = deque([0.0] * 45, maxlen=45)
        self.setMinimumHeight(170)

    def actualizar_valor(self, valor: float) -> None:
        valor_normalizado = max(0.0, min(valor, 3000.0))
        self._valores.append(valor_normalizado)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        if not self._valores:
            return

        ancho = max(1, self.width())
        alto = max(1, self.height())
        maximo = max(max(self._valores), 1.0)
        paso_x = ancho / max(1, len(self._valores) - 1)

        pintor = QPainter(self)
        pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
        pintor.fillRect(self.rect(), QColor("#0f1620"))

        grid_color = QColor(46, 59, 76)
        pintor.setPen(QPen(grid_color, 1))
        for porcentaje in (0.33, 0.66):
            y = int(alto * porcentaje)
            pintor.drawLine(0, y, ancho, y)

        puntos = []
        for indice, valor in enumerate(self._valores):
            x = indice * paso_x
            y = alto - ((valor / maximo) * (alto - 8)) - 4
            puntos.append((x, y))

        if len(puntos) >= 2:
            pintor.setPen(QPen(QColor("#ec4899"), 2))
            poligono = QPolygonF()
            for x, y in puntos:
                poligono.append(QPointF(x, y))
            pintor.drawPolyline(poligono)

class PanelRed(QFrame):
    def __init__(self, padre=None) -> None:
        super().__init__(padre)
        self.setObjectName("PanelRed")
        self.setMinimumHeight(300)

        self.etiqueta_titulo = QLabel("Red")
        self.etiqueta_titulo.setObjectName("TarjetaTitulo")

        self.etiqueta_interfaz = QLabel("Adaptador de red")
        self.etiqueta_interfaz.setObjectName("TarjetaDetalle")

        self.etiqueta_valor = QLabel("0.0 Kbps")
        self.etiqueta_valor.setObjectName("TarjetaValorTexto")

        self.etiqueta_detalle = QLabel("Subida 0.0 Kbps | Bajada 0.0 Kbps")
        self.etiqueta_detalle.setObjectName("TarjetaDetalle")
        self.etiqueta_detalle.setWordWrap(True)

        self.grafica = GraficaRed()

        contenido = QVBoxLayout(self)
        contenido.setContentsMargins(18, 16, 18, 16)
        contenido.setSpacing(8)
        contenido.addWidget(self.etiqueta_titulo)
        contenido.addWidget(self.etiqueta_interfaz)
        contenido.addWidget(self.etiqueta_valor)
        contenido.addWidget(self.grafica, 1)
        contenido.addWidget(self.etiqueta_detalle)

    def actualizar(self, subida_kbps: float, bajada_kbps: float, nombre_interfaz: str = "Red") -> None:
        total = subida_kbps + bajada_kbps
        self.etiqueta_interfaz.setText(nombre_interfaz)
        self.etiqueta_valor.setText(f"{total:.1f} Kbps")
        self.etiqueta_detalle.setText(f"Subida {subida_kbps:.1f} Kbps | Bajada {bajada_kbps:.1f} Kbps")
        self.grafica.actualizar_valor(total)