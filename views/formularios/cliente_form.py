"""
views/formularios/cliente_form.py
==================================
Formulario para crear/editar clientes con SQL Server.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from database.conexion import insertar_cliente_loja, actualizar_cliente_loja


class ClienteForm(QDialog):
    """
    Formulario para crear o editar un cliente.
    
    Señales:
        cliente_guardado: Se emite cuando se guarda exitosamente
    """
    
    cliente_guardado = pyqtSignal()
    
    def __init__(self, datos_usuario, cliente=None):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.cliente = cliente  # None para nuevo, dict para editar
        self.es_edicion = cliente is not None
        self.inicializar_ui()
        
        if self.es_edicion:
            self.cargar_datos_cliente()
            
    def inicializar_ui(self):
        """Configura la interfaz del formulario."""
        titulo = "Editar Cliente" if self.es_edicion else "Nuevo Cliente"
        self.setWindowTitle(titulo)
        self.setFixedSize(500, 450)
        self.setModal(True)
        self.setStyleSheet("background-color: white;")
        
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 30, 40, 30)
        layout_principal.setSpacing(15)
        self.setLayout(layout_principal)
        
        # Título
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(label_titulo)
        
        # Campos del formulario
        self.crear_campos(layout_principal)
        
        # Botones
        self.crear_botones(layout_principal)
        
    def crear_campos(self, layout_padre):
        """Crea los campos del formulario."""
        
        # NOMBRE
        label_nombre = QLabel("Nombre *")
        label_nombre.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo del cliente")
        self.input_nombre.setStyleSheet(self.estilo_input())
        self.input_nombre.setMinimumHeight(40)
        
        # DIRECCIÓN
        label_direccion = QLabel("Dirección")
        label_direccion.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección del cliente")
        self.input_direccion.setStyleSheet(self.estilo_input())
        self.input_direccion.setMinimumHeight(40)
        
        # TELÉFONO
        label_telefono = QLabel("Teléfono")
        label_telefono.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Número de teléfono")
        self.input_telefono.setStyleSheet(self.estilo_input())
        self.input_telefono.setMinimumHeight(40)
        
        # CORREO
        label_correo = QLabel("Correo Electrónico")
        label_correo.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("correo@ejemplo.com")
        self.input_correo.setStyleSheet(self.estilo_input())
        self.input_correo.setMinimumHeight(40)
        
        # Añadir al layout
        layout_padre.addWidget(label_nombre)
        layout_padre.addWidget(self.input_nombre)
        layout_padre.addWidget(label_direccion)
        layout_padre.addWidget(self.input_direccion)
        layout_padre.addWidget(label_telefono)
        layout_padre.addWidget(self.input_telefono)
        layout_padre.addWidget(label_correo)
        layout_padre.addWidget(self.input_correo)
        
    def crear_botones(self, layout_padre):
        """Crea los botones del formulario."""
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(10)
        layout_botones.addStretch()
        
        # Botón Cancelar
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setFixedSize(120, 45)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #7f8c8d;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ecf0f1; }
        """)
        btn_cancelar.setCursor(Qt.PointingHandCursor)
        btn_cancelar.clicked.connect(self.reject)
        
        # Botón Guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setFixedSize(120, 45)
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.clicked.connect(self.guardar_cliente)
        
        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_guardar)
        
        layout_padre.addStretch()
        layout_padre.addLayout(layout_botones)
        
    def estilo_input(self):
        """Retorna el estilo CSS para inputs."""
        return """
            QLineEdit {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """
        
    def cargar_datos_cliente(self):
        """Carga los datos del cliente en el formulario (modo edición)."""
        self.input_nombre.setText(self.cliente.get('nombre', ''))
        self.input_direccion.setText(self.cliente.get('direccion', ''))
        self.input_telefono.setText(self.cliente.get('telefono', ''))
        self.input_correo.setText(self.cliente.get('correo', ''))
        
    def validar_campos(self):
        """Valida que los campos estén correctamente llenados."""
        if not self.input_nombre.text().strip():
            QMessageBox.warning(self, "Validación", "El nombre del cliente es obligatorio")
            self.input_nombre.setFocus()
            return False
        
        return True
        
    def guardar_cliente(self):
        """Guarda el cliente en SQL Server."""
        if not self.validar_campos():
            return
        
        nombre = self.input_nombre.text().strip()
        direccion = self.input_direccion.text().strip()
        telefono = self.input_telefono.text().strip()
        correo = self.input_correo.text().strip()
        
        if self.es_edicion:
            # Actualizar cliente existente
            if actualizar_cliente_loja(self.cliente['id'], nombre, direccion, telefono, correo):
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
                self.cliente_guardado.emit()
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el cliente")
        else:
            # Insertar nuevo cliente
            if insertar_cliente_loja(nombre, direccion, telefono, correo):
                QMessageBox.information(self, "Éxito", "Cliente creado correctamente")
                self.cliente_guardado.emit()
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo crear el cliente")