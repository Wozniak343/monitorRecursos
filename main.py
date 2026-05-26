import sys
import logging
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from controladores.controlador_monitor import ControladorMonitor
from recursos.estilos import aplicar_estilos
from recursos.configuracion_logging import configurar_logging
from recursos.logo import obtener_icono_aplicacion

def configurar_app_id_windows() -> None:
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Wozniak343.monitorRecursos")
    except (AttributeError, OSError):
        pass


def main() -> int:
    configurar_app_id_windows()
    configurar_logging()
    logger = logging.getLogger("monitor_recursos")
    logger.info("Iniciando aplicación Monitor de Recursos")

    aplicacion = QApplication(sys.argv)
    aplicacion.setApplicationName("Monitor de Recursos")
    aplicacion.setApplicationDisplayName("Monitor de Recursos")
    aplicacion.setFont(QFont("Segoe UI", 9))
    icono_app = obtener_icono_aplicacion()
    if not icono_app.isNull():
        aplicacion.setWindowIcon(icono_app)
    aplicar_estilos(aplicacion)

    try:
        controlador = ControladorMonitor()
    except RuntimeError as error:
        print(error)
        return 1

    controlador.ventana.show()

    return aplicacion.exec()

if __name__ == "__main__":
    sys.exit(main())
