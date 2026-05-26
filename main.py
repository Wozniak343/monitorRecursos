import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from controladores.controlador_monitor import ControladorMonitor
from recursos.estilos import aplicar_estilos
from recursos.configuracion_logging import configurar_logging

def main() -> int:
    # Inicializar logging
    configurar_logging()
    logger = logging.getLogger("monitor_recursos")
    logger.info("Iniciando aplicación Monitor de Recursos")

    aplicacion = QApplication(sys.argv)
    aplicacion.setApplicationName("Monitor de Recursos")
    aplicacion.setApplicationDisplayName("Monitor de Recursos")
    aplicacion.setFont(QFont("Segoe UI", 9))
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
