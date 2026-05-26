from __future__ import annotations
from PySide6.QtWidgets import QApplication

ESTILO_OSCURO = """
QMainWindow {
    background-color: #0e141c;
    color: #e7e5e4;
}

QWidget {
    color: #e7e5e4;
    font-family: "Segoe UI", "Arial";
    font-size: 9.8pt;
}

QFrame#Encabezado,
QFrame#TarjetaRecurso,
QFrame#TarjetaInformativa,
QFrame#PanelRed,
QFrame#PanelProcesos,
QWidget#TarjetasContenedor {
    background-color: #121922;
    border: 1px solid #223041;
    border-radius: 12px;
}

QLabel#TituloPrincipal {
    font-size: 18pt;
    font-weight: 650;
}

QLabel#LogoPrincipal {
    padding: 4px;
}

QLabel#LogoSecundario {
    min-width: 16px;
}

QLabel#SubtituloPrincipal {
    color: #97a3b1;
    font-size: 10pt;
}

QLabel#TituloSeccion {
    font-size: 12pt;
    font-weight: 650;
}

QLabel#TarjetaTitulo {
    color: #97a3b1;
    font-size: 10pt;
    font-weight: 650;
}

QLabel#TarjetaValor {
    font-size: 21pt;
    font-weight: 650;
}

QLabel#TarjetaValorTexto {
    font-size: 20pt;
    font-weight: 650;
}

QLabel#DiscoNombre {
    color: #e7e5e4;
    font-size: 10pt;
    font-weight: 650;
}

QLabel#TarjetaDetalle {
    color: #c7d0db;
    font-size: 9.5pt;
}

QPushButton#BotonPrimario {
    background-color: #2f6fed;
    border: none;
    border-radius: 10px;
    padding: 9px 15px;
    font-weight: 650;
}

QPushButton#BotonPrimario:hover {
    background-color: #275fca;
}

QPushButton#BotonPrimario:pressed {
    background-color: #214da4;
}

QPushButton#BotonSecundario {
    background-color: #1a2330;
    border: 1px solid #314155;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 650;
}

QPushButton#BotonSecundario:hover {
    background-color: #223040;
}

QListWidget#ListaProcesos {
    background-color: #0f1620;
    border: 1px solid #223041;
    border-radius: 12px;
    padding: 6px;
    outline: none;
}

QListWidget#ListaProcesos::item {
    padding: 10px 8px;
    margin-bottom: 4px;
    border-radius: 8px;
}

QListWidget#ListaProcesos::item:selected {
    background-color: #2f6fed;
    color: #ffffff;
}

QTableWidget#TablaProcesos {
    background-color: #0f1620;
    border: 1px solid #223041;
    border-radius: 12px;
    gridline-color: #223041;
    selection-background-color: #2f6fed;
    selection-color: #ffffff;
}

QProgressBar#BarraDisco {
    background-color: #1a2230;
    border: 1px solid #314155;
    border-radius: 6px;
    height: 10px;
}

QProgressBar#BarraDisco::chunk {
    background-color: #5bb0ff;
    border-radius: 6px;
}

QProgressBar {
    background-color: #1a2230;
    border: 1px solid #314155;
    border-radius: 6px;
    height: 10px;
}

QProgressBar::chunk {
    background-color: #5bb0ff;
    border-radius: 6px;
}

QFrame#PanelRed {
    background-color: #121922;
    border: 1px solid #223041;
    border-radius: 12px;
}

QTableWidget {
    background-color: #0f1620;
    border: 1px solid #223041;
    border-radius: 14px;
    gridline-color: #223041;
    selection-background-color: #2f6fed;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #121922;
    color: #e7e5e4;
    border: none;
    border-bottom: 1px solid #223041;
    padding: 8px 10px;
    font-weight: 650;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:alternate {
    background-color: #121922;
}

QLabel#BarraEstado {
    color: #97a3b1;
    padding: 4px 2px;
}
"""

def aplicar_estilos(aplicacion: QApplication) -> None:
    aplicacion.setStyleSheet(ESTILO_OSCURO)
