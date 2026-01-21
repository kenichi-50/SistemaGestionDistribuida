"""
views/tablas/cliente_view.py
=============================
Vista simplificada de gestión de clientes.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QTableWidget, QPushButton, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt


class ClienteView(QMainWindow):
    """Vista de gestión de clientes."""
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.setWindowTitle("Gestión de Clientes")
        self.setMinimumSize(1000, 600)
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        widget_central.setLayout(layout)
        
        # Título
        label_titulo = QLabel("Gestión de Clientes")
        label_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(label_titulo)
        
        # Botones
        layout_botones = QHBoxLayout()
        
        btn_nuevo = QPushButton("+ Nuevo Cliente")
        btn_nuevo.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_nuevo.setCursor(Qt.PointingHandCursor)
        btn_nuevo.clicked.connect(lambda: print("TODO: Abrir formulario nuevo cliente"))
        
        layout_botones.addWidget(btn_nuevo)
        layout_botones.addStretch()
        layout.addLayout(layout_botones)
        
        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Cédula", "Teléfono", "Ciudad"])
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dcdde1;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.tabla)
        
        # TODO: Cargar datos de clientes desde SQL Server
        self.cargar_datos_mock()
        
    def cargar_datos_mock(self):
        """Carga datos de prueba."""
        # TODO: SELECT * FROM cliente WHERE ...
        clientes_mock = [
            (1, "Juan Pérez", "1234567890", "0987654321", "Quito"),
            (2, "María García", "0987654321", "0998877665", "Loja"),
            (3, "Carlos López", "1122334455", "0976543210", "Quito"),
        ]
        
        self.tabla.setRowCount(len(clientes_mock))
        for i, cliente in enumerate(clientes_mock):
            for j, dato in enumerate(cliente):
                from PyQt5.QtWidgets import QTableWidgetItem
                self.tabla.setItem(i, j, QTableWidgetItem(str(dato)))