from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
class PanelProcesos(QWidget):
    def __init__(self, padre=None) -> None:
        super().__init__(padre)

        self.tabla_procesos = QTableWidget(0, 4)
        self.tabla_procesos.setHorizontalHeaderLabels(["PID", "Proceso", "CPU %", "RAM MB"])
        self.tabla_procesos.verticalHeader().setVisible(False)
        self.tabla_procesos.setAlternatingRowColors(True)
        self.tabla_procesos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_procesos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_procesos.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        contenedor = QVBoxLayout(self)
        contenedor.setContentsMargins(0, 0, 0, 0)
        contenedor.addWidget(self.tabla_procesos)

    def actualizar_procesos(self, procesos: list[dict]) -> None:
        self.tabla_procesos.setRowCount(len(procesos))

        for indice_fila, proceso in enumerate(procesos):
            valores = [
                str(proceso["pid"]),
                proceso["nombre"],
                f"{proceso['cpu_porcentaje']:.1f}",
                f"{proceso['memoria_mb']:.1f}",
            ]

            for indice_columna, valor in enumerate(valores):
                elemento = QTableWidgetItem(valor)
                if indice_columna in (0, 2, 3):
                    elemento.setTextAlignment(int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter))
                self.tabla_procesos.setItem(indice_fila, indice_columna, elemento)
