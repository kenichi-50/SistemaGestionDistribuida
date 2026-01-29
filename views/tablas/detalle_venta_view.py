"""
views/tablas/detalle_venta_view.py
===================================
Vista de Detalle de Ventas.

Permite consultar los detalles (productos) de cualquier venta.
Disponible para ambos nodos (solo consulta).

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
                             QHeaderView, QMessageBox, QDialog, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.consultas_quito import obtener_detalle_venta_quito, obtener_ventas_quito
from database.consultas_loja import obtener_detalle_venta_loja, obtener_ventas_loja


class DetalleVentaView(QWidget):
    """
    Vista principal para consultar detalles de ventas.
    Muestra una lista de ventas y permite ver sus detalles.
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.init_ui()
        self.cargar_datos()
        self.showMaximized()

        
    def init_ui(self):
        """
        Inicializa la interfaz de usuario.
        """
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # ==================== ENCABEZADO ====================
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Detalle de Ventas")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2d3748;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Descripción
        desc_label = QLabel("Seleccione una venta para ver sus productos y detalles")
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setStyleSheet("color: #718096; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # ==================== BARRA DE BÚSQUEDA ====================
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar por cliente o ID de venta...")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3d5a80;
            }
        """)
        self.search_input.textChanged.connect(self.filtrar_datos)
        
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # ==================== BOTONES DE ACCIÓN ====================
        buttons_layout = QHBoxLayout()
        
        self.btn_ver_detalle = QPushButton("👁️ Ver Detalle")
        self.btn_ver_detalle.setFixedHeight(40)
        self.btn_ver_detalle.setCursor(Qt.PointingHandCursor)
        self.btn_ver_detalle.setEnabled(False)
        self.btn_ver_detalle.setStyleSheet("""
            QPushButton {
                background-color: #3d5a80;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #2e4660;
            }
            QPushButton:disabled {
                background-color: #cbd5e0;
                color: #a0aec0;
            }
        """)
        self.btn_ver_detalle.clicked.connect(self.ver_detalle)
        
        self.btn_actualizar = QPushButton("🔄 Actualizar")
        self.btn_actualizar.setFixedHeight(40)
        self.btn_actualizar.setCursor(Qt.PointingHandCursor)
        self.btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #718096;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f7fafc;
            }
        """)
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        
        buttons_layout.addWidget(self.btn_ver_detalle)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_actualizar)
        
        layout.addLayout(buttons_layout)
        
        # ==================== TABLA DE VENTAS ====================
        self.tabla = QTableWidget()
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(['ID Venta', 'Fecha', 'Cliente', 'Total', 'ID Empleado', 'ID Tienda'])
        
        # Configurar tabla
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Ajustar columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        # Estilo de la tabla
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #bee3f8;
                color: #2c5282;
            }
            QHeaderView::section {
                background-color: #f7fafc;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                color: #2d3748;
            }
        """)
        
        # Doble clic para ver detalle
        self.tabla.itemDoubleClicked.connect(self.ver_detalle)
        
        # Conectar evento de selección
        self.tabla.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.tabla)
        
        # ==================== INFORMACIÓN ====================
        self.info_label = QLabel("Mostrando 0 ventas")
        self.info_label.setStyleSheet("color: #718096; font-size: 13px; padding: 10px 0;")
        layout.addWidget(self.info_label)
        
    def cargar_datos(self):
        """
        Carga las ventas desde la base de datos según el nodo.
        """
        try:
            # Obtener ventas según el nodo
            if self.nodo == 'gestion':
                ventas = obtener_ventas_quito()
            else:  # operacion
                ventas = obtener_ventas_loja()
            
            # Guardar datos originales para filtrado
            self.datos_originales = ventas
            
            # Mostrar en tabla
            self.mostrar_datos(ventas)
            
        except Exception as e:
            print(f"Error al cargar ventas: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
            
    def mostrar_datos(self, datos):
        """
        Muestra los datos de ventas en la tabla.
        
        Args:
            datos (list): Lista de diccionarios con datos de ventas
        """
        self.tabla.setRowCount(0)
        
        for venta in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # ID Venta
            self.tabla.setItem(row, 0, QTableWidgetItem(str(venta['id'])))
            
            # Fecha (solo la parte de la fecha, sin hora)
            fecha = venta['fecha'].split(' ')[0] if venta['fecha'] else ''
            self.tabla.setItem(row, 1, QTableWidgetItem(fecha))
            
            # Cliente
            self.tabla.setItem(row, 2, QTableWidgetItem(venta['nombre_cliente']))
            
            # Total
            total_item = QTableWidgetItem(f"${venta['total']:.2f}")
            total_item.setForeground(Qt.darkGreen)
            total_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.tabla.setItem(row, 3, total_item)
            
            # ID Empleado
            self.tabla.setItem(row, 4, QTableWidgetItem(str(venta['id_empleado'])))
            
            # ID Tienda
            self.tabla.setItem(row, 5, QTableWidgetItem(str(venta['id_tienda'])))
        
        # Actualizar info
        self.info_label.setText(f"Mostrando {len(datos)} ventas")
        
    def filtrar_datos(self):
        """
        Filtra los datos según el texto de búsqueda.
        """
        if not hasattr(self, 'datos_originales'):
            return
            
        texto = self.search_input.text().lower()
        
        if not texto:
            self.mostrar_datos(self.datos_originales)
            return
        
        # Filtrar por ID o nombre de cliente
        datos_filtrados = []
        for venta in self.datos_originales:
            if (texto in str(venta['id']).lower() or 
                texto in venta['nombre_cliente'].lower()):
                datos_filtrados.append(venta)
        
        self.mostrar_datos(datos_filtrados)
        
    def on_selection_changed(self):
        """
        Maneja el cambio de selección en la tabla.
        """
        hay_seleccion = len(self.tabla.selectedItems()) > 0
        self.btn_ver_detalle.setEnabled(hay_seleccion)
        
    def ver_detalle(self):
        """
        Abre el diálogo para ver el detalle de la venta seleccionada.
        """
        row = self.tabla.currentRow()
        if row < 0:
            return
            
        # Obtener datos de la venta
        id_venta = int(self.tabla.item(row, 0).text())
        fecha = self.tabla.item(row, 1).text()
        cliente = self.tabla.item(row, 2).text()
        total = self.tabla.item(row, 3).text()
        
        # Crear y mostrar diálogo con los detalles
        dialog = DetalleVentaDialog(
            self.datos_usuario, 
            id_venta, 
            fecha, 
            cliente, 
            total
        )
        dialog.exec_()


# ==============================================================================
# DIÁLOGO PARA MOSTRAR EL DETALLE DE UNA VENTA
# ==============================================================================

class DetalleVentaDialog(QDialog):
    """
    Diálogo para mostrar el detalle completo de una venta.
    Muestra los productos vendidos con sus cantidades y precios.
    """
    
    def __init__(self, datos_usuario, id_venta, fecha, cliente, total):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.id_venta = id_venta
        self.fecha = fecha
        self.cliente = cliente
        self.total = total
        self.init_ui()
        self.cargar_datos()
        
    def init_ui(self):
        """
        Inicializa la interfaz del diálogo.
        """
        self.setWindowTitle(f"Detalle de Venta #{self.id_venta}")
        self.setFixedSize(800, 500)
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # ==================== ENCABEZADO ====================
        header_frame = QLabel()
        header_frame.setStyleSheet("""
            background-color: #f7fafc;
            border-radius: 8px;
            padding: 15px;
        """)
        
        header_layout = QVBoxLayout()
        
        # Título
        title = QLabel(f"Venta #{self.id_venta}")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #2d3748;")
        
        # Información de la venta
        info_layout = QHBoxLayout()
        
        fecha_label = QLabel(f"📅 Fecha: {self.fecha}")
        fecha_label.setFont(QFont("Segoe UI", 11))
        fecha_label.setStyleSheet("color: #4a5568;")
        
        cliente_label = QLabel(f"👤 Cliente: {self.cliente}")
        cliente_label.setFont(QFont("Segoe UI", 11))
        cliente_label.setStyleSheet("color: #4a5568;")
        
        total_label = QLabel(f"💰 Total: {self.total}")
        total_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        total_label.setStyleSheet("color: #22543d;")
        
        info_layout.addWidget(fecha_label)
        info_layout.addWidget(cliente_label)
        info_layout.addStretch()
        info_layout.addWidget(total_label)
        
        header_layout.addWidget(title)
        header_layout.addLayout(info_layout)
        
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
        # ==================== TABLA DE PRODUCTOS ====================
        productos_label = QLabel("Productos Vendidos:")
        productos_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        productos_label.setStyleSheet("color: #2d3748; margin-top: 10px;")
        layout.addWidget(productos_label)
        
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            'Línea', 
            'ID Producto', 
            'Nombre del Producto', 
            'Precio Unitario',
            'Cantidad'
        ])
        
        # Configurar tabla
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        
        # Ajustar columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # Estilo de la tabla
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #edf2f7;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #cbd5e0;
                font-weight: bold;
                color: #2d3748;
            }
        """)
        
        layout.addWidget(self.tabla)
        
        # ==================== INFORMACIÓN ADICIONAL ====================
        self.info_label = QLabel("Cargando productos...")
        self.info_label.setStyleSheet("color: #718096; font-size: 12px;")
        layout.addWidget(self.info_label)
        
        # ==================== BOTÓN CERRAR ====================
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setFixedHeight(40)
        btn_cerrar.setCursor(Qt.PointingHandCursor)
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #3d5a80;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2e4660;
            }
        """)
        btn_cerrar.clicked.connect(self.close)
        
        layout.addWidget(btn_cerrar, alignment=Qt.AlignRight)
        
    def cargar_datos(self):
        """
        Carga los detalles de la venta desde la base de datos.
        """
        try:
            # Obtener detalles según el nodo
            if self.nodo == 'gestion':
                detalles = obtener_detalle_venta_quito(self.id_venta)
            else:
                detalles = obtener_detalle_venta_loja(self.id_venta)
            
            # Mostrar en tabla
            self.mostrar_detalles(detalles)
            
        except Exception as e:
            print(f"Error al cargar detalle de venta: {e}")
            self.info_label.setText("❌ Error al cargar los productos")
            QMessageBox.critical(self, "Error", f"Error al cargar detalles: {str(e)}")
            
    def mostrar_detalles(self, detalles):
        """
        Muestra los detalles en la tabla.
        
        Args:
            detalles (list): Lista de diccionarios con detalles de la venta
        """
        self.tabla.setRowCount(0)
        
        if not detalles:
            self.info_label.setText("⚠️ No se encontraron productos para esta venta")
            return
        
        for detalle in detalles:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # Línea
            self.tabla.setItem(row, 0, QTableWidgetItem(str(detalle['linea_id'])))
            
            # ID Producto
            self.tabla.setItem(row, 1, QTableWidgetItem(str(detalle['id_producto'])))
            
            # Nombre Producto
            self.tabla.setItem(row, 2, QTableWidgetItem(detalle['nombre_producto']))
            
            # Precio Unitario
            precio = detalle.get('precio_unitario', 0)
            precio_text = f"${precio:.2f}" if precio > 0 else "N/A"
            precio_item = QTableWidgetItem(precio_text)
            precio_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.tabla.setItem(row, 3, precio_item)
            
            # Cantidad
            cantidad_val = detalle.get('cantidad', 1)
            cantidad_item = QTableWidgetItem(str(cantidad_val))
            cantidad_item.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(row, 4, cantidad_item)
        
        # Actualizar info
        self.info_label.setText(f"✓ Se encontraron {len(detalles)} productos en esta venta")