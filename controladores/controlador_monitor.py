from __future__ import annotations
from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QMessageBox
from modelos.monitor_sistema import MonitorSistema
from vistas.ventana_principal import VentanaPrincipal
import logging

logger = logging.getLogger("monitor_recursos")

class ControladorMonitor(QObject):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Iniciando ControladorMonitor")
        self.modelo = MonitorSistema()
        self.ventana = VentanaPrincipal()
        self.temporizador = QTimer(self)
        self.temporizador.setInterval(2000)
        self.temporizador.timeout.connect(self.actualizar)
        self.ventana.boton_actualizar.clicked.connect(self.actualizar)
        self.ventana.boton_finalizar_proceso.clicked.connect(self.finalizar_proceso_seleccionado)

        self.actualizar()
        self.temporizador.start()

    def actualizar(self) -> None:
        logger.debug("Actualizando datos del sistema")
        resumen = self.modelo.obtener_resumen_sistema()
        procesos = self.modelo.obtener_procesos_mas_pesados()
        self.ventana.actualizar_datos(resumen, procesos)
        self.ventana.mostrar_estado("Datos actualizados automaticamente cada 2 segundos")
        logger.info("Datos actualizados")

    def finalizar_proceso_seleccionado(self) -> None:
        pid = self.ventana.proceso_seleccionado()
        if pid is None:
            QMessageBox.information(self.ventana, "Finalizar proceso", "Selecciona un proceso primero.")
            return

        try:
            self.modelo.finalizar_proceso(pid)
        except (PermissionError, ProcessLookupError, OSError) as error:
            logger.warning("Error al finalizar proceso %s: %s", pid, error)
            QMessageBox.warning(self.ventana, "Finalizar proceso", f"No se pudo finalizar el proceso: {error}")
            return

        self.actualizar()
        logger.info("Proceso %s finalizado", pid)
        QMessageBox.information(self.ventana, "Finalizar proceso", f"Proceso {pid} finalizado.")

