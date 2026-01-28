# ==============================================================================
# ARCHIVO: views/formularios/tienda_form.py
# ==============================================================================
"""Formulario para Tiendas (solo Quito)."""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.consultas_quito import insertar_tienda_quito, actualizar_tienda_quito


class TiendaForm(QDialog):
    def __init__(self, datos_usuario, modo='nuevo', datos=None):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.modo = modo
        self.datos = datos or {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Nueva Tienda" if self.modo == 'nuevo' else "Editar Tienda")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Título
        title = QLabel("Nueva Tienda" if self.modo == 'nuevo' else "Editar Tienda")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Nombre
        layout.addWidget(QLabel("Nombre"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese el nombre de la tienda")
        self.input_nombre.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_nombre.setText(self.datos.get('nombre', ''))
        layout.addWidget(self.input_nombre)
        
        # Ciudad
        layout.addWidget(QLabel("Ciudad"))
        self.input_ciudad = QLineEdit()
        self.input_ciudad.setPlaceholderText("Ingrese la ciudad")
        self.input_ciudad.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_ciudad.setText(self.datos.get('ciudad', ''))
        layout.addWidget(self.input_ciudad)
        
        # Dirección
        layout.addWidget(QLabel("Dirección"))
        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Ingrese la dirección")
        self.input_direccion.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_direccion.setText(self.datos.get('direccion', ''))
        layout.addWidget(self.input_direccion)
        
        # Teléfono
        layout.addWidget(QLabel("Teléfono"))
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Ingrese el teléfono")
        self.input_telefono.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_telefono.setText(self.datos.get('telefono', ''))
        layout.addWidget(self.input_telefono)
        
        layout.addStretch()
        
        # Botones
        buttons = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setFixedHeight(40)
        btn_cancelar.clicked.connect(self.reject)
        
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setFixedHeight(40)
        btn_guardar.setStyleSheet("background-color: #3d5a80; color: white; font-weight: bold;")
        btn_guardar.clicked.connect(self.guardar)
        
        buttons.addWidget(btn_cancelar)
        buttons.addWidget(btn_guardar)
        layout.addLayout(buttons)
        
    def guardar(self):
        nombre = self.input_nombre.text().strip()
        ciudad = self.input_ciudad.text().strip()
        direccion = self.input_direccion.text().strip()
        telefono = self.input_telefono.text().strip()
        
        if not nombre or not ciudad:
            QMessageBox.warning(self, "Error", "Nombre y Ciudad son obligatorios")
            return
            
        if self.modo == 'nuevo':
            ok = insertar_tienda_quito(nombre, ciudad, direccion, telefono)
        else:
            ok = actualizar_tienda_quito(self.datos['id'], nombre, ciudad, direccion, telefono)
            
        if ok:
            QMessageBox.information(self, "Éxito", "Tienda guardada correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la tienda")


