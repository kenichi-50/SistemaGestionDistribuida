"""
views/tablas/producto_view.py
==============================
Vista de gestión de productos con tabla, filtros y CRUD.
Basada en la Imagen 5 del diseño proporcionado.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QComboBox, QFrame,
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.permisos import tiene_permiso
from data_mock.productos import obtener_productos_mock
from views.formularios.producto_form import ProductoForm


class ProductoView(QMainWindow):
    """
    Vista de gestión de productos.
    Muestra tabla con productos y permite CRUD según permisos.
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.productos = []
        self.producto_form = None
        self.inicializar_ui()
        self.cargar_datos()
        
    def inicializar_ui(self):
        """Configura la interfaz de la vista de productos."""
        self.setWindowTitle("Sistema de Gestión Distribuida - Productos")
        self.setMinimumSize(1000, 600)
        
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        widget_central.setLayout(layout_principal)
        
        # Crear barra superior
        self.crear_barra_superior(layout_principal)
        
        # Crear área de contenido
        self.crear_area_contenido(layout_principal)
        
    def crear_barra_superior(self, layout_padre):
        """Crea la barra superior con breadcrumb y usuario."""
        barra = QFrame()
        barra.setFixedHeight(70)
        barra.setStyleSheet("background-color: white; border-bottom: 1px solid #dcdde1;")
        
        layout_barra = QHBoxLayout()
        layout_barra.setContentsMargins(30, 15, 30, 15)
        barra.setLayout(layout_barra)
        
        # Breadcrumb
        nodo_texto = "Nodo de Gestión" if self.nodo == "gestion" else "Nodo de Operación"
        ciudad = self.datos_usuario['ciudad']
        breadcrumb = QLabel(f"Sistema de Gestión Distribuida  >  {nodo_texto}  >  Nodo: {ciudad}")
        breadcrumb.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        
        layout_barra.addWidget(breadcrumb)
        layout_barra.addStretch()
        
        # Usuario
        label_usuario = QLabel(f"👤 {self.datos_usuario['usuario']}")
        label_usuario.setStyleSheet("font-size: 14px; color: #2c3e50; margin-right: 15px;")
        
        # Botón cerrar sesión
        btn_cerrar = QPushButton("Cerrar Sesión")
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
        """Crea el área principal con tabla y controles."""
        frame_contenido = QFrame()
        frame_contenido.setStyleSheet("background-color: #ecf0f1;")
        
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(40, 30, 40, 30)
        layout_contenido.setSpacing(20)
        frame_contenido.setLayout(layout_contenido)
        
        # Título
        label_titulo = QLabel("Productos")
        label_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout_contenido.addWidget(label_titulo)
        
        # Barra de búsqueda y botones
        self.crear_barra_busqueda(layout_contenido)
        
        # Filtros
        self.crear_barra_filtros(layout_contenido)
        
        # Tabla
        self.crear_tabla(layout_contenido)
        
        layout_padre.addWidget(frame_contenido)
        
    def crear_barra_busqueda(self, layout_padre):
        """Crea la barra de búsqueda con botones de acción."""
        frame_busqueda = QFrame()
        frame_busqueda.setStyleSheet("background-color: transparent;")
        
        layout_busqueda = QHBoxLayout()
        layout_busqueda.setContentsMargins(0, 0, 0, 0)
        frame_busqueda.setLayout(layout_busqueda)
        
        # Campo de búsqueda
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("🔍 Buscar...")
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
        
        # Botones de acción
        puede_crear = tiene_permiso(self.nodo, 'producto', 'crear')
        puede_editar = tiene_permiso(self.nodo, 'producto', 'editar')
        puede_eliminar = tiene_permiso(self.nodo, 'producto', 'eliminar')
        
        # Botón Nuevo
        self.btn_nuevo = QPushButton("+ Nuevo")
        self.btn_nuevo.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.btn_nuevo.setCursor(Qt.PointingHandCursor if puede_crear else Qt.ForbiddenCursor)
        self.btn_nuevo.setEnabled(puede_crear)
        self.btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)
        
        # Botón Editar
        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
                border-color: #95a5a6;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #bdc3c7;
            }
        """)
        self.btn_editar.setCursor(Qt.PointingHandCursor if puede_editar else Qt.ForbiddenCursor)
        self.btn_editar.setEnabled(puede_editar)
        self.btn_editar.clicked.connect(self.editar_seleccionado)
        
        # Botón Eliminar
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
                border-color: #95a5a6;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #bdc3c7;
            }
        """)
        self.btn_eliminar.setCursor(Qt.PointingHandCursor if puede_eliminar else Qt.ForbiddenCursor)
        self.btn_eliminar.setEnabled(puede_eliminar)
        self.btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        
        layout_busqueda.addWidget(self.btn_nuevo)
        layout_busqueda.addWidget(self.btn_editar)
        layout_busqueda.addWidget(self.btn_eliminar)
        
        layout_padre.addWidget(frame_busqueda)
        
    def crear_barra_filtros(self, layout_padre):
        """Crea la barra de filtros."""
        frame_filtros = QFrame()
        frame_filtros.setStyleSheet("background-color: transparent;")
        
        layout_filtros = QHBoxLayout()
        layout_filtros.setContentsMargins(0, 0, 0, 0)
        frame_filtros.setLayout(layout_filtros)
        
        label_filtrar = QLabel("Filtrar por:")
        label_filtrar.setStyleSheet("font-size: 13px; color: #7f8c8d;")
        
        # Filtro 1
        self.combo_filtro1 = QComboBox()
        self.combo_filtro1.addItems(["- Seleccionar -", "Categoría", "Marca", "Precio"])
        self.combo_filtro1.setStyleSheet("""
            QComboBox {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 8px 15px;
                background-color: white;
                min-width: 150px;
            }
        """)
        
        # Filtro 2
        self.combo_filtro2 = QComboBox()
        self.combo_filtro2.addItems(["- Seleccionar -", "Stock Alto", "Stock Bajo"])
        self.combo_filtro2.setStyleSheet("""
            QComboBox {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 8px 15px;
                background-color: white;
                min-width: 150px;
            }
        """)
        
        # Botón actualizar
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
            }
        """)
        btn_actualizar.setCursor(Qt.PointingHandCursor)
        btn_actualizar.clicked.connect(self.cargar_datos)
        
        layout_filtros.addWidget(label_filtrar)
        layout_filtros.addWidget(self.combo_filtro1)
        layout_filtros.addWidget(self.combo_filtro2)
        layout_filtros.addStretch()
        layout_filtros.addWidget(btn_actualizar)
        
        layout_padre.addWidget(frame_filtros)
        
    def crear_tabla(self, layout_padre):
        """Crea la tabla de productos."""
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Código", "Precio", "Stock", "Actualización", "⋮"
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
        self.tabla.setColumnWidth(3, 100)
        self.tabla.setColumnWidth(4, 80)
        self.tabla.setColumnWidth(5, 120)
        self.tabla.setColumnWidth(6, 50)
        
        # Configuraciones adicionales
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)
        
        layout_padre.addWidget(self.tabla)
        
    def cargar_datos(self):
        """
        Carga los datos de productos en la tabla.
        
        ⚠️ TODO: Reemplazar por consulta SQL Server:
        
        SELECT p.idProducto, p.nombre, p.codigo, p.precio, 
               i.stock, i.fechaActualizacion
        FROM producto p
        LEFT JOIN inventario i ON p.idProducto = i.fkIdProducto
        WHERE i.fkIdTienda = ?  -- Filtrar por tienda del nodo
        ORDER BY p.nombre
        """
        # TODO: Reemplazar por consulta SQL Server
        self.productos = obtener_productos_mock()
        self.actualizar_tabla()
        
    def actualizar_tabla(self):
        """Actualiza la tabla con los productos cargados."""
        self.tabla.setRowCount(0)
        
        for producto in self.productos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # ID
            self.tabla.setItem(row, 0, QTableWidgetItem(str(producto['id'])))
            
            # Nombre
            self.tabla.setItem(row, 1, QTableWidgetItem(producto['nombre']))
            
            # Código
            self.tabla.setItem(row, 2, QTableWidgetItem(producto['codigo']))
            
            # Precio
            self.tabla.setItem(row, 3, QTableWidgetItem(f"${producto['precio']:.2f}"))
            
            # Stock
            self.tabla.setItem(row, 4, QTableWidgetItem(str(producto['stock'])))
            
            # Fecha actualización
            self.tabla.setItem(row, 5, QTableWidgetItem(producto['fecha_actualizacion']))
            
            # Menú opciones
            btn_menu = QPushButton("⋮")
            btn_menu.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-size: 18px;
                    color: #7f8c8d;
                }
                QPushButton:hover {
                    color: #2c3e50;
                }
            """)
            btn_menu.setCursor(Qt.PointingHandCursor)
            self.tabla.setCellWidget(row, 6, btn_menu)
            
    def filtrar_tabla(self):
        """Filtra la tabla según el texto de búsqueda."""
        texto_busqueda = self.input_buscar.text().lower()
        
        for row in range(self.tabla.rowCount()):
            mostrar = False
            for col in range(self.tabla.columnCount() - 1):
                item = self.tabla.item(row, col)
                if item and texto_busqueda in item.text().lower():
                    mostrar = True
                    break
            
            self.tabla.setRowHidden(row, not mostrar)
            
    def abrir_formulario_nuevo(self):
        """
        Abre el formulario para crear un nuevo producto.
        
        ⚠️ TODO: El formulario guardará en SQL Server
        """
        self.producto_form = ProductoForm(self.datos_usuario)
        self.producto_form.producto_guardado.connect(self.cargar_datos)
        self.producto_form.show()
        
    def editar_seleccionado(self):
        """Edita el producto seleccionado."""
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada >= 0:
            producto_id = int(self.tabla.item(fila_seleccionada, 0).text())
            producto = next((p for p in self.productos if p['id'] == producto_id), None)
            
            if producto:
                self.producto_form = ProductoForm(self.datos_usuario, producto)
                self.producto_form.producto_guardado.connect(self.cargar_datos)
                self.producto_form.show()
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un producto para editar")
            
    def eliminar_seleccionado(self):
        """
        Elimina el producto seleccionado.
        
        ⚠️ TODO: Ejecutar DELETE en SQL Server
        """
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada >= 0:
            producto_nombre = self.tabla.item(fila_seleccionada, 1).text()
            
            respuesta = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar el producto '{producto_nombre}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                # TODO: DELETE FROM producto WHERE idProducto = ?
                self.tabla.removeRow(fila_seleccionada)
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un producto para eliminar")