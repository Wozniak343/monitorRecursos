from __future__ import annotations
from PySide6.QtWidgets import QFrame, QLabel, QProgressBar, QScrollArea, QVBoxLayout, QWidget

class PanelDiscos(QWidget):
    def __init__(self, padre=None) -> None:
        super().__init__(padre)
        self.setMinimumHeight(280)
        self.contenido = QWidget()
        self.contenido.setObjectName("PanelDiscosContenido")
        self.disposicion = QVBoxLayout(self.contenido)
        self.disposicion.setContentsMargins(0, 0, 0, 0)
        self.disposicion.setSpacing(10)

        self.etiqueta_titulo = QLabel("Discos")
        self.etiqueta_titulo.setObjectName("TarjetaTitulo")

        self.etiqueta_resumen = QLabel("Uso en tiempo real de cada partición")
        self.etiqueta_resumen.setObjectName("TarjetaDetalle")
        self.etiqueta_resumen.setWordWrap(True)

        self.area = QScrollArea()
        self.area.setWidgetResizable(True)
        self.area.setFrameShape(QFrame.Shape.NoFrame)
        self.area.setWidget(self.contenido)

        contenedor = QVBoxLayout(self)
        contenedor.setContentsMargins(18, 16, 18, 16)
        contenedor.setSpacing(10)
        contenedor.addWidget(self.etiqueta_titulo)
        contenedor.addWidget(self.etiqueta_resumen)
        contenedor.addWidget(self.area)

    def actualizar_discos(self, discos: list[dict]) -> None:
        while self.disposicion.count():
            elemento = self.disposicion.takeAt(0)
            widget = elemento.widget()
            if widget is not None:
                widget.deleteLater()

        if not discos:
            etiqueta_vacia = QLabel("No se encontraron discos montados")
            etiqueta_vacia.setObjectName("TarjetaDetalle")
            self.disposicion.addWidget(etiqueta_vacia)
            return

        for disco in discos:
            fila = QWidget()
            fila_disposicion = QVBoxLayout(fila)
            fila_disposicion.setContentsMargins(0, 0, 0, 0)
            fila_disposicion.setSpacing(6)

            nombre = QLabel(f'{disco["dispositivo"]} · {disco["punto_montaje"]} · {disco["tipo"]}')
            nombre.setObjectName("DiscoNombre")
            detalle = QLabel(f'{disco["porcentaje"]:.0f}%  |  {disco["usado_gb"]:.1f} / {disco["total_gb"]:.1f} GB')
            detalle.setObjectName("TarjetaDetalle")

            barra = QProgressBar()
            barra.setRange(0, 100)
            barra.setValue(int(round(disco["porcentaje"])))
            barra.setTextVisible(False)
            barra.setObjectName("BarraDisco")

            fila_disposicion.addWidget(nombre)
            fila_disposicion.addWidget(detalle)
            fila_disposicion.addWidget(barra)
            self.disposicion.addWidget(fila)
