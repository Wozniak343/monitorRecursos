from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QVBoxLayout,
    QWidget,
)
from vistas.componente_tarjeta import TarjetaRecurso
from vistas.panel_discos import PanelDiscos
from vistas.panel_red import PanelRed

class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Monitor de Recursos")
        self.resize(980, 720)
        self.setMinimumSize(860, 640)

        contenedor_central = QWidget()
        self.setCentralWidget(contenedor_central)

        self.area_desplazable = QScrollArea()
        self.area_desplazable.setWidgetResizable(True)
        self.area_desplazable.setFrameShape(QFrame.Shape.NoFrame)

        self.contenido = QWidget()
        self.area_desplazable.setWidget(self.contenido)

        distribucion_principal = QVBoxLayout(contenedor_central)
        distribucion_principal.setContentsMargins(16, 16, 16, 16)
        distribucion_principal.setSpacing(0)
        distribucion_principal.addWidget(self.area_desplazable)

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        distribucion = QVBoxLayout(self.contenido)
        distribucion.setContentsMargins(0, 0, 0, 0)
        distribucion.setSpacing(16)

        encabezado = QFrame()
        encabezado.setObjectName("Encabezado")
        contenido_encabezado = QHBoxLayout(encabezado)
        contenido_encabezado.setContentsMargins(18, 16, 18, 16)
        contenido_encabezado.setSpacing(12)

        bloque_texto = QVBoxLayout()
        etiqueta_titulo = QLabel("Monitor de Recursos")
        etiqueta_titulo.setObjectName("TituloPrincipal")
        bloque_texto.addWidget(etiqueta_titulo)

        self.boton_actualizar = QPushButton("Actualizar ahora")
        self.boton_actualizar.setObjectName("BotonPrimario")
        self.boton_actualizar.setCursor(Qt.CursorShape.PointingHandCursor)

        contenido_encabezado.addLayout(bloque_texto)
        contenido_encabezado.addStretch(1)
        contenido_encabezado.addWidget(self.boton_actualizar)

        distribucion.addWidget(encabezado)

        tarjetas_contenedor = QFrame()
        tarjetas_contenedor.setObjectName("TarjetasContenedor")
        rejilla_tarjetas = QGridLayout(tarjetas_contenedor)
        rejilla_tarjetas.setContentsMargins(0, 0, 0, 0)
        rejilla_tarjetas.setHorizontalSpacing(12)
        rejilla_tarjetas.setVerticalSpacing(12)
        rejilla_tarjetas.setColumnStretch(0, 1)
        rejilla_tarjetas.setColumnStretch(1, 1)
        rejilla_tarjetas.setColumnStretch(2, 1)

        self.tarjeta_cpu = TarjetaRecurso("CPU", "Uso actual")
        self.tarjeta_ram = TarjetaRecurso("Memoria RAM", "Uso actual")
        self.tarjeta_gpu = TarjetaRecurso("GPU", "Uso y temperatura")
        self.panel_discos = PanelDiscos()
        self.panel_red = PanelRed()
        self.panel_procesos = QFrame()
        self.panel_procesos.setObjectName("TarjetaInformativa")
        self.panel_procesos.setMinimumHeight(340)
        disposicion_procesos = QVBoxLayout(self.panel_procesos)
        disposicion_procesos.setContentsMargins(18, 16, 18, 16)
        disposicion_procesos.setSpacing(10)
        titulo_procesos = QLabel("Procesos activos")
        titulo_procesos.setObjectName("TarjetaTitulo")
        self.texto_procesos = QLabel("Lista de procesos en tiempo real")
        self.texto_procesos.setObjectName("TarjetaDetalle")
        self.texto_procesos.setWordWrap(True)
        self.tabla_procesos = QTableWidget(0, 4)
        self.tabla_procesos.setObjectName("TablaProcesos")
        self.tabla_procesos.setHorizontalHeaderLabels(["PID", "Proceso", "CPU %", "RAM MB"])
        self.tabla_procesos.verticalHeader().setVisible(False)
        self.tabla_procesos.setAlternatingRowColors(True)
        self.tabla_procesos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_procesos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_procesos.setMinimumHeight(240)
        self.tabla_procesos.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.boton_finalizar_proceso = QPushButton("Finalizar seleccionado")
        self.boton_finalizar_proceso.setObjectName("BotonSecundario")
        disposicion_procesos.addWidget(titulo_procesos)
        disposicion_procesos.addWidget(self.texto_procesos)
        disposicion_procesos.addWidget(self.tabla_procesos, 1)
        disposicion_procesos.addWidget(self.boton_finalizar_proceso)

        rejilla_tarjetas.addWidget(self.tarjeta_cpu, 0, 0)
        rejilla_tarjetas.addWidget(self.tarjeta_gpu, 0, 1)
        rejilla_tarjetas.addWidget(self.tarjeta_ram, 0, 2)
        rejilla_tarjetas.addWidget(self.panel_discos, 1, 0, 1, 2)
        rejilla_tarjetas.addWidget(self.panel_red, 1, 2)

        distribucion.addWidget(tarjetas_contenedor)

        self.panel_procesos.setMinimumHeight(360)
        distribucion.addWidget(self.panel_procesos)

        self.etiqueta_estado = QLabel("Listo para iniciar la monitorizacion")
        self.etiqueta_estado.setObjectName("BarraEstado")
        self.etiqueta_estado.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        distribucion.addWidget(self.etiqueta_estado)

    def actualizar_datos(self, resumen: dict, procesos: list[dict]) -> None:
        self.tarjeta_cpu.actualizar(
            resumen["cpu_porcentaje"],
            resumen["cpu_nombre"],
        )
        self.tarjeta_ram.actualizar(
            resumen["memoria_porcentaje"],
            f'{resumen["memoria_usada_gb"]:.1f} GB / {resumen["memoria_total_gb"]:.1f} GB',
        )
        self.tarjeta_gpu.actualizar(
            resumen["gpu_porcentaje"],
            resumen["gpu_nombre"],
        )

        self.panel_discos.actualizar_discos(resumen.get("discos", []))
        self.panel_red.actualizar(
            resumen["red_subida_kbps"],
            resumen["red_bajada_kbps"],
            resumen.get("nombre_interfaz_red", "Red"),
        )

        self.tabla_procesos.setUpdatesEnabled(False)
        try:
            self.tabla_procesos.setRowCount(len(procesos))
            for fila, proceso in enumerate(procesos):
                self.tabla_procesos.setItem(fila, 0, QTableWidgetItem(str(proceso["pid"])))
                self.tabla_procesos.setItem(fila, 1, QTableWidgetItem(proceso["nombre"]))
                self.tabla_procesos.setItem(fila, 2, QTableWidgetItem(f'{proceso["cpu_porcentaje"]:.1f}'))
                self.tabla_procesos.setItem(fila, 3, QTableWidgetItem(f'{proceso["memoria_mb"]:.1f}'))
        finally:
            self.tabla_procesos.setUpdatesEnabled(True)

        self.texto_procesos.setText(f'{resumen["cantidad_procesos"]} procesos activos. Selecciona uno para finalizarlo.')

    def mostrar_estado(self, mensaje: str) -> None:
        self.etiqueta_estado.setText(mensaje)

    def proceso_seleccionado(self) -> int | None:
        fila = self.tabla_procesos.currentRow()
        if fila < 0:
            return None
        elemento = self.tabla_procesos.item(fila, 0)
        if elemento is None:
            return None
        return int(elemento.text())
