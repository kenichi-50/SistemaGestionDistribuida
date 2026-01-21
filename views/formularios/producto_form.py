"""
views/formularios/producto_form.py
===================================
Formulario para crear/editar productos.
Basado en la Imagen 4 del diseño proporcionado.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class ProductoForm(QDialog):
    """
    Formulario para crear o editar un producto.
    
    Señales:
        producto_guardado: Se emite cuando se guarda exitosamente
    """
    
    producto_guardado = pyqtSignal()
    
    def __init__(self, datos_usuario, producto=None):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.producto = producto  # None para nuevo, dict para editar
        self.es_edicion = producto is not None
        self.inicializar_ui()
        
        if self.es_edicion:
            self.cargar_datos_producto()
            
    def inicializar_ui(self):
        """Configura la interfaz del formulario."""
        # Configuración del diálogo
        titulo = "Editar Producto" if self.es_edicion else "Nuevo Producto"
        self.setWindowTitle(titulo)
        self.setFixedSize(600, 500)
        self.setModal(True)
        self.setStyleSheet("background-color: white;")
        
        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 30, 40, 30)
        layout_principal.setSpacing(20)
        self.setLayout(layout_principal)
        
        # Título
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout_principal.addWidget(label_titulo)
        
        # Campos del formulario
        self.crear_campos(layout_principal)
        
        # Botones
        self.crear_botones(layout_principal)
        
    def crear_campos(self, layout_padre):
        """Crea los campos del formulario."""
        
        # ========== NOMBRE ==========
        label_nombre = QLabel("Nombre")
        label_nombre.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese el nombre del producto")
        self.input_nombre.setStyleSheet(self.estilo_input())
        self.input_nombre.setMinimumHeight(40)
        
        # ========== DESCRIPCIÓN ==========
        label_descripcion = QLabel("Descripción")
        label_descripcion.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_descripcion = QTextEdit()
        self.input_descripcion.setPlaceholderText("Descripción breve del producto")
        self.input_descripcion.setStyleSheet(self.estilo_input())
        self.input_descripcion.setMaximumHeight(80)
        
        # ========== CÓDIGO ==========
        label_codigo = QLabel("Código")
        label_codigo.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Ingrese el código del producto")
        self.input_codigo.setStyleSheet(self.estilo_input())
        self.input_codigo.setMinimumHeight(40)
        
        # ========== PRECIO Y STOCK (en horizontal) ==========
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(15)
        
        # Precio
        layout_precio = QVBoxLayout()
        layout_precio.setSpacing(5)
        
        label_precio = QLabel("Precio")
        label_precio.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Ingrese el precio del producto")
        self.input_precio.setStyleSheet(self.estilo_input())
        self.input_precio.setMinimumHeight(40)
        
        layout_precio.addWidget(label_precio)
        layout_precio.addWidget(self.input_precio)
        
        # Stock
        layout_stock = QVBoxLayout()
        layout_stock.setSpacing(5)
        
        label_stock = QLabel("Stock")
        label_stock.setStyleSheet("font-size: 13px; font-weight: 500; color: #2c3e50;")
        
        self.input_stock = QLineEdit()
        self.input_stock.setPlaceholderText("Cantidad inicial en stock")
        self.input_stock.setStyleSheet(self.estilo_input())
        self.input_stock.setMinimumHeight(40)
        
        layout_stock.addWidget(label_stock)
        layout_stock.addWidget(self.input_stock)
        
        layout_horizontal.addLayout(layout_precio)
        layout_horizontal.addLayout(layout_stock)
        
        # Añadir todo al layout padre
        layout_padre.addWidget(label_nombre)
        layout_padre.addWidget(self.input_nombre)
        layout_padre.addWidget(label_descripcion)
        layout_padre.addWidget(self.input_descripcion)
        layout_padre.addWidget(label_codigo)
        layout_padre.addWidget(self.input_codigo)
        layout_padre.addLayout(layout_horizontal)
        
    def crear_botones(self, layout_padre):
        """Crea los botones del formulario."""
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(10)
        
        # Espacio flexible a la izquierda
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
            QPushButton:hover {
                background-color: #ecf0f1;
                border-color: #95a5a6;
            }
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
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.clicked.connect(self.guardar_producto)
        
        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_guardar)
        
        layout_padre.addStretch()
        layout_padre.addLayout(layout_botones)
        
    def estilo_input(self):
        """Retorna el estilo CSS para inputs."""
        return """
            QLineEdit, QTextEdit {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """
        
    def cargar_datos_producto(self):
        """Carga los datos del producto en el formulario (modo edición)."""
        self.input_nombre.setText(self.producto['nombre'])
        self.input_descripcion.setPlainText(self.producto.get('descripcion', ''))
        self.input_codigo.setText(self.producto['codigo'])
        self.input_precio.setText(str(self.producto['precio']))
        self.input_stock.setText(str(self.producto.get('stock', 0)))
        
    def validar_campos(self):
        """
        Valida que los campos estén correctamente llenados.
        
        Returns:
            bool: True si es válido, False si no
        """
        # Validar nombre
        if not self.input_nombre.text().strip():
            QMessageBox.warning(self, "Validación", "El nombre del producto es obligatorio")
            self.input_nombre.setFocus()
            return False
        
        # Validar código
        if not self.input_codigo.text().strip():
            QMessageBox.warning(self, "Validación", "El código del producto es obligatorio")
            self.input_codigo.setFocus()
            return False
        
        # Validar precio
        try:
            precio = float(self.input_precio.text().strip())
            if precio <= 0:
                raise ValueError()
        except:
            QMessageBox.warning(self, "Validación", "El precio debe ser un número mayor a 0")
            self.input_precio.setFocus()
            return False
        
        # Validar stock
        try:
            stock = int(self.input_stock.text().strip())
            if stock < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self, "Validación", "El stock debe ser un número entero positivo")
            self.input_stock.setFocus()
            return False
        
        return True
        
    def guardar_producto(self):
        """
        Guarda el producto en la base de datos.
        
        ⚠️ TODO: Implementar INSERT/UPDATE en SQL Server
        
        Para NUEVO producto:
        INSERT INTO producto (nombre, descripcion, codigo, precio)
        VALUES (?, ?, ?, ?)
        
        Para EDITAR producto:
        UPDATE producto
        SET nombre = ?, descripcion = ?, codigo = ?, precio = ?
        WHERE idProducto = ?
        
        Además, actualizar el inventario:
        INSERT/UPDATE inventario (fkIdProducto, fkIdTienda, stock)
        """
        # Validar campos
        if not self.validar_campos():
            return
        
        # Obtener valores
        nombre = self.input_nombre.text().strip()
        descripcion = self.input_descripcion.toPlainText().strip()
        codigo = self.input_codigo.text().strip()
        precio = float(self.input_precio.text().strip())
        stock = int(self.input_stock.text().strip())
        
        # TODO: Aquí va la lógica de INSERT/UPDATE a SQL Server
        print("=" * 60)
        print("TODO: GUARDAR EN SQL SERVER")
        print("=" * 60)
        
        if self.es_edicion:
            print(f"UPDATE producto WHERE idProducto = {self.producto['id']}")
            print(f"  nombre = '{nombre}'")
            print(f"  descripcion = '{descripcion}'")
            print(f"  codigo = '{codigo}'")
            print(f"  precio = {precio}")
            print(f"UPDATE inventario SET stock = {stock}")
        else:
            print("INSERT INTO producto")
            print(f"  (nombre, descripcion, codigo, precio)")
            print(f"  VALUES ('{nombre}', '{descripcion}', '{codigo}', {precio})")
            print(f"INSERT INTO inventario (fkIdProducto, fkIdTienda, stock)")
            print(f"  VALUES (LAST_INSERT_ID(), {self.datos_usuario.get('id_tienda', 1)}, {stock})")
        
        print("=" * 60)
        
        # Mostrar mensaje de éxito
        mensaje = "Producto actualizado correctamente" if self.es_edicion else "Producto creado correctamente"
        QMessageBox.information(self, "Éxito", mensaje)
        
        # Emitir señal de guardado
        self.producto_guardado.emit()
        
        # Cerrar formulario
        self.accept()