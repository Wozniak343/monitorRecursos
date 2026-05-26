from __future__ import annotations
from threading import Lock

from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot
from PySide6.QtWidgets import QMessageBox
from modelos.monitor_sistema import MonitorSistema
from vistas.ventana_principal import VentanaPrincipal
import logging

logger = logging.getLogger("monitor_recursos")


class _ActualizadorMonitor(QObject):
    datos_listos = Signal(object, object)
    error = Signal(str)

    def __init__(self, modelo: MonitorSistema, cantidad_procesos: int, bloqueo: Lock) -> None:
        super().__init__()
        self._modelo = modelo
        self._cantidad_procesos = cantidad_procesos
        self._bloqueo = bloqueo

    @Slot()
    def actualizar(self) -> None:
        try:
            with self._bloqueo:
                resumen = self._modelo.obtener_resumen_sistema()
                procesos = self._modelo.obtener_procesos_mas_pesados(cantidad=self._cantidad_procesos)
        except Exception as error:  # noqa: BLE001
            logger.exception("Error al actualizar datos del sistema")
            self.error.emit(str(error))
            return

        self.datos_listos.emit(resumen, procesos)


class ControladorMonitor(QObject):
    PROCESOS_VISIBLES = 50
    solicitar_actualizacion_interna = Signal()

    def __init__(self) -> None:
        super().__init__()
        logger.info("Iniciando ControladorMonitor")
        self.modelo = MonitorSistema()
        self.ventana = VentanaPrincipal()
        self._bloqueo_modelo = Lock()
        self._actualizacion_en_curso = False
        self._actualizacion_pendiente = False

        self._hilo_actualizador = QThread(self)
        self._trabajador_actualizador = _ActualizadorMonitor(
            self.modelo,
            self.PROCESOS_VISIBLES,
            self._bloqueo_modelo,
        )
        self._trabajador_actualizador.moveToThread(self._hilo_actualizador)
        self._trabajador_actualizador.datos_listos.connect(self._aplicar_datos)
        self._trabajador_actualizador.error.connect(self._mostrar_error_actualizacion)
        self.solicitar_actualizacion_interna.connect(self._trabajador_actualizador.actualizar)
        self._hilo_actualizador.finished.connect(self._trabajador_actualizador.deleteLater)
        self._hilo_actualizador.start()

        self.temporizador = QTimer(self)
        self.temporizador.setInterval(2000)
        self.temporizador.timeout.connect(self.solicitar_actualizacion)
        self.ventana.boton_actualizar.clicked.connect(self.solicitar_actualizacion)
        self.ventana.boton_finalizar_proceso.clicked.connect(self.finalizar_proceso_seleccionado)
        self.ventana.destroyed.connect(self._detener_hilo_actualizador)

        self.solicitar_actualizacion()
        self.temporizador.start()

    @Slot()
    def solicitar_actualizacion(self) -> None:
        if self._actualizacion_en_curso:
            self._actualizacion_pendiente = True
            return

        self._actualizacion_en_curso = True
        self.ventana.mostrar_estado("Actualizando datos...")
        self.solicitar_actualizacion_interna.emit()

    @Slot(object, object)
    def _aplicar_datos(self, resumen: dict, procesos: list[dict]) -> None:
        self._actualizacion_en_curso = False
        logger.debug("Actualizando datos del sistema")
        self.ventana.actualizar_datos(resumen, procesos)
        self.ventana.mostrar_estado("Datos actualizados automaticamente cada 2 segundos")
        logger.info("Datos actualizados")
        if self._actualizacion_pendiente:
            self._actualizacion_pendiente = False
            self.solicitar_actualizacion()

    @Slot(str)
    def _mostrar_error_actualizacion(self, mensaje: str) -> None:
        self._actualizacion_en_curso = False
        self.ventana.mostrar_estado(f"Error al actualizar: {mensaje}")
        logger.error("Error al actualizar datos del sistema: %s", mensaje)
        if self._actualizacion_pendiente:
            self._actualizacion_pendiente = False
            self.solicitar_actualizacion()

    def finalizar_proceso_seleccionado(self) -> None:
        pid = self.ventana.proceso_seleccionado()
        if pid is None:
            QMessageBox.information(self.ventana, "Finalizar proceso", "Selecciona un proceso primero.")
            return

        try:
            with self._bloqueo_modelo:
                self.modelo.finalizar_proceso(pid)
        except (PermissionError, ProcessLookupError, OSError) as error:
            logger.warning("Error al finalizar proceso %s: %s", pid, error)
            QMessageBox.warning(self.ventana, "Finalizar proceso", f"No se pudo finalizar el proceso: {error}")
            return

        self.solicitar_actualizacion()
        logger.info("Proceso %s finalizado", pid)
        QMessageBox.information(self.ventana, "Finalizar proceso", f"Proceso {pid} finalizado.")

    def _detener_hilo_actualizador(self) -> None:
        if self._hilo_actualizador.isRunning():
            self._hilo_actualizador.quit()
            self._hilo_actualizador.wait()

