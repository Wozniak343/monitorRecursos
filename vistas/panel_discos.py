from __future__ import annotations
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QProgressBar, QScrollArea, QVBoxLayout, QWidget
from recursos.logo import obtener_logo
class PanelDiscos(QWidget):
    def __init__(self, padre=None) -> None:
        super().__init__(padre)
        self.setMinimumHeight(280)
        self.contenido = QWidget()
        self.contenido.setObjectName("PanelDiscosContenido")
        self.disposicion = QVBoxLayout(self.contenido)
        self.disposicion.setContentsMargins(0, 0, 0, 0)
        self.disposicion.setSpacing(10)
        self._filas_por_disco: dict[str, tuple[QWidget, QLabel, QLabel, QProgressBar]] = {}
        self._etiqueta_vacia: QLabel | None = None

        encabezado = QHBoxLayout()
        encabezado.setContentsMargins(0, 0, 0, 0)
        encabezado.setSpacing(8)
        icono = QLabel()
        icono.setPixmap(obtener_logo(18))
        icono.setObjectName("LogoSecundario")

        self.etiqueta_titulo = QLabel("Discos")
        self.etiqueta_titulo.setObjectName("TarjetaTitulo")
        encabezado.addWidget(icono)
        encabezado.addWidget(self.etiqueta_titulo)
        encabezado.addStretch(1)

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
        contenedor.addLayout(encabezado)
        contenedor.addWidget(self.etiqueta_resumen)
        contenedor.addWidget(self.area)

    def actualizar_discos(self, discos: list[dict]) -> None:
        if not discos:
            self._limpiar_filas_discos()
            if self._etiqueta_vacia is None:
                self._etiqueta_vacia = QLabel("No se encontraron discos montados")
                self._etiqueta_vacia.setObjectName("TarjetaDetalle")
                self.disposicion.addWidget(self._etiqueta_vacia)
            return

        if self._etiqueta_vacia is not None:
            self._etiqueta_vacia.deleteLater()
            self._etiqueta_vacia = None

        claves_presentes: set[str] = set()
        for disco in discos:
            clave = f'{disco["dispositivo"]}|{disco["punto_montaje"]}'
            claves_presentes.add(clave)

            if clave not in self._filas_por_disco:
                self._filas_por_disco[clave] = self._crear_fila()
                self.disposicion.addWidget(self._filas_por_disco[clave][0])

            fila, nombre, detalle, barra = self._filas_por_disco[clave]
            nombre.setText(f'{disco["dispositivo"]} · {disco["punto_montaje"]} · {disco["tipo"]}')
            detalle.setText(f'{disco["porcentaje"]:.0f}%  |  {disco["usado_gb"]:.1f} / {disco["total_gb"]:.1f} GB')
            barra.setValue(int(round(disco["porcentaje"])))
            fila.show()

        for clave in list(self._filas_por_disco.keys()):
            if clave in claves_presentes:
                continue
            fila, _, _, _ = self._filas_por_disco.pop(clave)
            fila.deleteLater()

    def _crear_fila(self) -> tuple[QWidget, QLabel, QLabel, QProgressBar]:
        fila = QWidget()
        fila_disposicion = QVBoxLayout(fila)
        fila_disposicion.setContentsMargins(0, 0, 0, 0)
        fila_disposicion.setSpacing(6)

        nombre = QLabel()
        nombre.setObjectName("DiscoNombre")
        detalle = QLabel()
        detalle.setObjectName("TarjetaDetalle")

        barra = QProgressBar()
        barra.setRange(0, 100)
        barra.setTextVisible(False)
        barra.setObjectName("BarraDisco")

        fila_disposicion.addWidget(nombre)
        fila_disposicion.addWidget(detalle)
        fila_disposicion.addWidget(barra)
        return fila, nombre, detalle, barra

    def _limpiar_filas_discos(self) -> None:
        for clave, (fila, _, _, _) in list(self._filas_por_disco.items()):
            fila.deleteLater()
            del self._filas_por_disco[clave]
