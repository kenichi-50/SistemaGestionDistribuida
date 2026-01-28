# ==============================================================================
# ARCHIVO: views/formularios/cliente_form.py
# ==============================================================================
"""Formulario para Clientes."""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QFont
from database.consultas_quito import insertar_cliente_quito, actualizar_cliente_quito
from database.consultas_loja import insertar_cliente_loja, actualizar_cliente_loja


class ClienteForm(QDialog):
    def __init__(self, datos_usuario, modo='nuevo', datos=None):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.modo = modo
        self.datos = datos or {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Nuevo Cliente" if self.modo == 'nuevo' else "Editar Cliente")
        self.setFixedSize(500, 450)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        title = QLabel("Nuevo Cliente" if self.modo == 'nuevo' else "Editar Cliente")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Nombre
        layout.addWidget(QLabel("Nombre"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo del cliente")
        self.input_nombre.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_nombre.setText(self.datos.get('nombre', ''))
        layout.addWidget(self.input_nombre)
        
        # Dirección
        layout.addWidget(QLabel("Dirección"))
        self.input_direccion = QLineEdit()
        self.input_direccion.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_direccion.setText(self.datos.get('direccion', ''))
        layout.addWidget(self.input_direccion)
        
        # Teléfono
        layout.addWidget(QLabel("Teléfono"))
        self.input_telefono = QLineEdit()
        self.input_telefono.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_telefono.setText(self.datos.get('telefono', ''))
        layout.addWidget(self.input_telefono)
        
        # Correo
        layout.addWidget(QLabel("Correo"))
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("ejemplo@correo.com")
        self.input_correo.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_correo.setText(self.datos.get('correo', ''))
        layout.addWidget(self.input_correo)
        
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
        direccion = self.input_direccion.text().strip()
        telefono = self.input_telefono.text().strip()
        correo = self.input_correo.text().strip()
        
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return
            
        if self.modo == 'nuevo':
            if self.nodo == 'gestion':
                ok = insertar_cliente_quito(nombre, direccion, telefono, correo)
            else:
                ok = insertar_cliente_loja(nombre, direccion, telefono, correo)
        else:
            if self.nodo == 'gestion':
                ok = actualizar_cliente_quito(self.datos['id'], nombre, direccion, telefono, correo)
            else:
                ok = actualizar_cliente_loja(self.datos['id'], nombre, direccion, telefono, correo)
                
        if ok:
            QMessageBox.information(self, "Éxito", "Cliente guardado correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar el cliente")


