"""
views/tablas/producto_view.py
==============================
Vista de productos con SQL Server.

NODO LOJA: SOLO LECTURA
Los productos son gestionados desde Quito.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QComboBox, QFrame,
                             QMessageBox)
from PyQt5.QtCore import Qt
from database.conexion import obtener_productos_loja, obtener_inventario_loja


class ProductoView(QMainWindow):
    """
    Vista de productos (SOLO LECTURA en Nodo Loja).
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.productos = []
        self.inventario = {}
        self.inicializar_ui()
        self.cargar_datos()
        
    def inicializar_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("Productos - Nodo Loja (Solo Lectura)")
        self.setMinimumSize(1000, 600)
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        widget_central.setLayout(layout_principal)
        
        self.crear_barra_superior(layout_principal)
        self.crear_area_contenido(layout_principal)
        
    def crear_barra_superior(self, layout_padre):
        """Crea la barra superior."""
        barra = QFrame()
        barra.setFixedHeight(70)
        barra.setStyleSheet("background-color: white; border-bottom: 1px solid #dcdde1;")
        
        layout_barra = QHBoxLayout()
        layout_barra.setContentsMargins(30, 15, 30, 15)
        barra.setLayout(layout_barra)
        
        breadcrumb = QLabel(f"Sistema de Gestión Distribuida > Nodo: {self.datos_usuario['ciudad']} > Productos")
        breadcrumb.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        
        layout_barra.addWidget(breadcrumb)
        layout_barra.addStretch()
        
        label_usuario = QLabel(f"👤 {self.datos_usuario['usuario']}")
        label_usuario.setStyleSheet("font-size: 14px; color: #2c3e50; margin-right: 15px;")
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2c3e50; }
        """)
        btn_cerrar.setCursor(Qt.PointingHandCursor)
        btn_cerrar.clicked.connect(self.close)
        
        layout_barra.addWidget(label_usuario)
        layout_barra.addWidget(btn_cerrar)
        
        layout_padre.addWidget(barra)
        
    def crear_area_contenido(self, layout_padre):
        """Crea el área principal."""
        frame_contenido = QFrame()
        frame_contenido.setStyleSheet("background-color: #ecf0f1;")
        
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(40, 30, 40, 30)
        layout_contenido.setSpacing(20)
        frame_contenido.setLayout(layout_contenido)
        
        # Título con advertencia de solo lectura
        label_titulo = QLabel("Productos (Solo Lectura)")
        label_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        
        label_info = QLabel("ℹ️ Los productos son gestionados desde el Nodo de Gestión (Quito)")
        label_info.setStyleSheet("""
            font-size: 12px;
            color: #e67e22;
            background-color: #fef5e7;
            padding: 8px 12px;
            border-radius: 5px;
            border-left: 4px solid #e67e22;
        """)
        
        layout_contenido.addWidget(label_titulo)
        layout_contenido.addWidget(label_info)
        
        # Barra de búsqueda (sin botones de edición)
        self.crear_barra_busqueda(layout_contenido)
        
        # Tabla
        self.crear_tabla(layout_contenido)
        
        layout_padre.addWidget(frame_contenido)
        
    def crear_barra_busqueda(self, layout_padre):
        """Crea la barra de búsqueda."""
        frame_busqueda = QFrame()
        frame_busqueda.setStyleSheet("background-color: transparent;")
        
        layout_busqueda = QHBoxLayout()
        layout_busqueda.setContentsMargins(0, 0, 0, 0)
        frame_busqueda.setLayout(layout_busqueda)
        
        # Campo de búsqueda
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("🔍 Buscar producto...")
        self.input_buscar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus { border: 1px solid #3498db; }
        """)
        self.input_buscar.setMaximumWidth(300)
        self.input_buscar.textChanged.connect(self.filtrar_tabla)
        
        layout_busqueda.addWidget(self.input_buscar)
        layout_busqueda.addStretch()
        
        # Solo botón Actualizar (sin Nuevo/Editar/Eliminar)
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.setStyleSheet("""
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
        btn_actualizar.setCursor(Qt.PointingHandCursor)
        btn_actualizar.clicked.connect(self.cargar_datos)
        
        layout_busqueda.addWidget(btn_actualizar)
        
        layout_padre.addWidget(frame_busqueda)
        
    def crear_tabla(self, layout_padre):
        """Crea la tabla de productos."""
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Marca", "Modelo", "Categoría", "Precio", "Stock Mínimo"
        ])
        
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #e8f4f8;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #dcdde1;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        
        # Configurar columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        
        self.tabla.setColumnWidth(0, 60)
        self.tabla.setColumnWidth(2, 120)
        self.tabla.setColumnWidth(3, 120)
        self.tabla.setColumnWidth(4, 120)
        self.tabla.setColumnWidth(5, 100)
        self.tabla.setColumnWidth(6, 100)
        
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)
        
        layout_padre.addWidget(self.tabla)
        
    def cargar_datos(self):
        """Carga los datos desde SQL Server."""
        print("\n🔄 Cargando productos desde SQL Server...")
        self.productos = obtener_productos_loja()
        
        # Cargar inventario para mostrar stock
        print("🔄 Cargando inventario...")
        inventario_lista = obtener_inventario_loja()
        self.inventario = {item['id_producto']: item['stock'] for item in inventario_lista}
        
        self.actualizar_tabla()
        print(f"✓ {len(self.productos)} productos cargados\n")
        
    def actualizar_tabla(self):
        """Actualiza la tabla con los productos cargados."""
        self.tabla.setRowCount(0)
        
        for producto in self.productos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            self.tabla.setItem(row, 0, QTableWidgetItem(str(producto['id'])))
            self.tabla.setItem(row, 1, QTableWidgetItem(producto['nombre']))
            self.tabla.setItem(row, 2, QTableWidgetItem(producto.get('marca', '')))
            self.tabla.setItem(row, 3, QTableWidgetItem(producto.get('modelo', '')))
            self.tabla.setItem(row, 4, QTableWidgetItem(producto.get('categoria', '')))
            self.tabla.setItem(row, 5, QTableWidgetItem(f"${producto['precio']:.2f}"))
            self.tabla.setItem(row, 6, QTableWidgetItem(str(producto.get('stock_minimo', 0))))
            
    def filtrar_tabla(self):
        """Filtra la tabla según el texto de búsqueda."""
        texto_busqueda = self.input_buscar.text().lower()
        
        for row in range(self.tabla.rowCount()):
            mostrar = False
            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(row, col)
                if item and texto_busqueda in item.text().lower():
                    mostrar = True
                    break
            
            self.tabla.setRowHidden(row, not mostrar)