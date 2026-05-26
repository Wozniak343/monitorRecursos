import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from controladores.controlador_monitor import ControladorMonitor
from recursos.estilos import aplicar_estilos

def main() -> int:
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
