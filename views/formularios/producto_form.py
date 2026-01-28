# ==============================================================================
# ARCHIVO: views/formularios/producto_form.py
# ==============================================================================
"""Formulario para Productos (solo Quito puede editar)."""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QDoubleSpinBox, QSpinBox)
from PyQt5.QtGui import QFont
from database.consultas_quito import insertar_producto_quito, actualizar_producto_quito
from PyQt5.QtWidgets import QComboBox


class ProductoForm(QDialog):
    def __init__(self, datos_usuario, modo='nuevo', datos=None):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.modo = modo
        self.datos = datos or {}
        self.init_ui()

        
    def init_ui(self):
        self.setWindowTitle("Nuevo Producto" if self.modo == 'nuevo' else "Editar Producto")
        self.setFixedSize(700, 850)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        title = QLabel("Nuevo Producto" if self.modo == 'nuevo' else "Editar Producto")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Nombre
        layout.addWidget(QLabel("Nombre"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese el nombre del producto")
        self.input_nombre.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_nombre.setText(self.datos.get('nombre', ''))
        layout.addWidget(self.input_nombre)
        
        # Marca
        layout.addWidget(QLabel("Marca"))
        self.input_marca = QLineEdit()
        self.input_marca.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_marca.setText(self.datos.get('marca', ''))
        layout.addWidget(self.input_marca)
        
        # Modelo
        layout.addWidget(QLabel("Modelo"))
        self.input_modelo = QLineEdit()
        self.input_modelo.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_modelo.setText(self.datos.get('modelo', ''))
        layout.addWidget(self.input_modelo)
        
        # Categoría
        layout.addWidget(QLabel("Categoría"))
        self.input_categoria = QLineEdit()
        self.input_categoria.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_categoria.setText(self.datos.get('categoria', ''))
        layout.addWidget(self.input_categoria)
        
        # Precio y Stock en fila
        row = QHBoxLayout()
        
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("Precio ($)"))
        self.input_precio = QDoubleSpinBox()
        self.input_precio.setRange(0, 999999)
        self.input_precio.setDecimals(2)
        self.input_precio.setPrefix("$ ")
        self.input_precio.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_precio.setValue(self.datos.get('precio', 0))
        col1.addWidget(self.input_precio)
        
        col2 = QVBoxLayout()
        col2.addWidget(QLabel("Stock Mínimo"))
        self.input_stock = QSpinBox()
        self.input_stock.setRange(0, 9999)
        self.input_stock.setFixedHeight(40)
        if self.modo == 'editar':
            self.input_stock.setValue(self.datos.get('stock_minimo', 0))
        col2.addWidget(self.input_stock)

        row.addLayout(col1)
        row.addLayout(col2)

        layout.addLayout(row) 
        row_extra = QHBoxLayout()

        col_costo = QVBoxLayout()
        col_costo.addWidget(QLabel("Costo Logístico ($)"))
        self.input_costo = QDoubleSpinBox()
        self.input_costo.setRange(0, 999999)
        self.input_costo.setDecimals(2)
        self.input_costo.setPrefix("$ ")
        self.input_costo.setFixedHeight(40)
        col_costo.addWidget(self.input_costo)

        col_margen = QVBoxLayout()
        col_margen.addWidget(QLabel("Margen de Ganancia (%)"))
        self.input_margen = QDoubleSpinBox()
        self.input_margen.setRange(0, 100)
        self.input_margen.setDecimals(2)
        self.input_margen.setSuffix(" %")
        self.input_margen.setFixedHeight(40)
        col_margen.addWidget(self.input_margen)

        row_extra.addLayout(col_costo)
        row_extra.addLayout(col_margen)

        layout.addLayout(row_extra)

        layout.addWidget(QLabel("Clasificación de Planeación"))
        self.input_clasificacion = QComboBox()
        self.input_clasificacion.addItems([
            "Stock Regular",
            "Alta Prioridad",
            "Venta Rápida",
            "Baja Rotación"
        ])
        self.input_clasificacion.setFixedHeight(40)
        layout.addWidget(self.input_clasificacion)

        
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
        marca = self.input_marca.text().strip()
        modelo = self.input_modelo.text().strip()
        categoria = self.input_categoria.text().strip()
        precio = self.input_precio.value()
        stock_min = self.input_stock.value()

        costo = self.input_costo.value()
        margen = self.input_margen.value()
        clasificacion = self.input_clasificacion.currentText()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        if self.modo == 'nuevo':
            ok = insertar_producto_quito(
                nombre, marca, modelo, categoria,
                precio, stock_min,
                costo, margen, clasificacion
            )
        else:
            ok = actualizar_producto_quito(
                self.datos['id'], nombre, marca, modelo, categoria,
                precio, stock_min,
                costo, margen, clasificacion
            )

        if ok:
            QMessageBox.information(self, "Éxito", "Producto guardado correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar el producto")

