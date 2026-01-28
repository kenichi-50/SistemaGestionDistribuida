"""
views/tablas/inventario_view.py
================================
Vista de consulta de Inventario.

El inventario es SOLO LECTURA - se actualiza automáticamente con las ventas.
Cada nodo solo ve su inventario local.

Características:
- Vista de solo lectura
- Resalta productos con stock bajo (en rojo)
- Búsqueda por producto
- Actualización automática

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
                             QHeaderView, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush
from database.consultas_quito import obtener_inventario_quito
from database.consultas_loja import obtener_inventario_loja


class InventarioView(QWidget):
    """
    Vista para consultar el Inventario local.
    Solo lectura - se actualiza automáticamente con las ventas.
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
        
        title_label = QLabel("Inventario")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2d3748;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # ==================== ALERTA INFORMATIVA ====================
        alert_frame = QFrame()
        alert_frame.setStyleSheet("""
            QFrame {
                background-color: #ebf8ff;
                border-left: 4px solid #3182ce;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        alert_layout = QHBoxLayout()
        alert_frame.setLayout(alert_layout)
        
        # Icono
        icon_label = QLabel("ℹ️")
        icon_label.setFont(QFont("Segoe UI", 20))
        icon_label.setFixedWidth(30)
        
        # Mensaje
        info_text = QLabel(
            "El inventario se actualiza automáticamente con cada venta.\n"
            "Los productos con stock bajo aparecen resaltados en rojo."
        )
        info_text.setFont(QFont("Segoe UI", 11))
        info_text.setStyleSheet("color: #2c5282;")
        info_text.setWordWrap(True)
        
        alert_layout.addWidget(icon_label)
        alert_layout.addWidget(info_text)
        
        layout.addWidget(alert_frame)
        
        # ==================== BARRA DE BÚSQUEDA ====================
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar producto por id...")
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
        
        # Botón Actualizar
        self.btn_actualizar = QPushButton("🔄 Actualizar")
        self.btn_actualizar.setFixedHeight(40)
        self.btn_actualizar.setCursor(Qt.PointingHandCursor)
        self.btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #3d5a80;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2e4660;
            }
        """)
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        
        # Botón Ver Solo Stock Bajo
        self.btn_stock_bajo = QPushButton("⚠️ Ver Stock Bajo")
        self.btn_stock_bajo.setFixedHeight(40)
        self.btn_stock_bajo.setCursor(Qt.PointingHandCursor)
        self.btn_stock_bajo.setCheckable(True)
        self.btn_stock_bajo.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #e53e3e;
                border: 2px solid #e53e3e;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fff5f5;
            }
            QPushButton:checked {
                background-color: #e53e3e;
                color: white;
            }
        """)
        self.btn_stock_bajo.clicked.connect(self.toggle_stock_bajo)
        
        buttons_layout.addWidget(self.btn_actualizar)
        buttons_layout.addWidget(self.btn_stock_bajo)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # ==================== TABLA ====================
        self.tabla = QTableWidget()
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            'ID Tienda', 
            'ID Producto', 
            'Stock Actual', 
            'Stock Mínimo',
            'Última Actualización'
        ])
        
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
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
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
        
        layout.addWidget(self.tabla)
        
        # ==================== ESTADÍSTICAS ====================
        stats_layout = QHBoxLayout()
        
        # Total de productos
        self.label_total = QLabel("Total: 0 productos")
        self.label_total.setStyleSheet("""
            color: #2d3748;
            font-size: 13px;
            font-weight: bold;
            padding: 10px;
            background-color: #f7fafc;
            border-radius: 5px;
        """)
        
        # Productos con stock bajo
        self.label_stock_bajo = QLabel("Stock bajo: 0")
        self.label_stock_bajo.setStyleSheet("""
            color: #e53e3e;
            font-size: 13px;
            font-weight: bold;
            padding: 10px;
            background-color: #fff5f5;
            border-radius: 5px;
        """)
        
        stats_layout.addWidget(self.label_total)
        stats_layout.addWidget(self.label_stock_bajo)
        stats_layout.addStretch()
        
        layout.addLayout(stats_layout)
        
    def cargar_datos(self):
        """
        Carga el inventario desde la base de datos según el nodo.
        """
        try:
            # Obtener inventario según el nodo
            if self.nodo == 'gestion':
                inventario = obtener_inventario_quito()
            else:  # operacion
                inventario = obtener_inventario_loja()
            
            # Guardar datos originales para filtrado
            self.datos_originales = inventario
            
            # Mostrar en tabla
            self.mostrar_datos(inventario)
            
            # Actualizar estadísticas
            self.actualizar_estadisticas(inventario)
            
        except Exception as e:
            print(f"Error al cargar inventario: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
            
    def mostrar_datos(self, datos):
        """
        Muestra los datos en la tabla.
        
        Args:
            datos (list): Lista de diccionarios con datos de inventario
        """
        self.tabla.setRowCount(0)
        
        for item in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # ID Tienda
            self.tabla.setItem(row, 0, QTableWidgetItem(str(item['id_tienda'])))
            
            # ID Producto
            self.tabla.setItem(row, 1, QTableWidgetItem(str(item['id_producto'])))
            

            # Stock Actual
            stock = item['stock']
            stock_minimo = item.get('stock_minimo', 0)
            stock_item = QTableWidgetItem(str(stock))
            stock_item.setTextAlignment(Qt.AlignCenter)
            stock_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            # Resaltar si el stock está bajo
            if stock < stock_minimo:
                stock_item.setBackground(QBrush(QColor("#fed7d7")))
                stock_item.setForeground(QBrush(QColor("#c53030")))
            elif stock == 0:
                stock_item.setBackground(QBrush(QColor("#fc8181")))
                stock_item.setForeground(QBrush(QColor("#ffffff")))
            else:
                stock_item.setForeground(QBrush(QColor("#38a169")))
            
            self.tabla.setItem(row, 2, stock_item)
            
            # Stock Mínimo
            stock_min_item = QTableWidgetItem(str(stock_minimo))
            stock_min_item.setTextAlignment(Qt.AlignCenter)
            stock_min_item.setForeground(QBrush(QColor("#718096")))
            self.tabla.setItem(row, 3, stock_min_item)
            
            # Última Actualización
            fecha = item['fecha_actualizacion'].split(' ')[0] if item['fecha_actualizacion'] else 'N/A'
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setForeground(QBrush(QColor("#718096")))
            self.tabla.setItem(row, 4, fecha_item)
        
    def actualizar_estadisticas(self, datos):
        """
        Actualiza las estadísticas del inventario.
        
        Args:
            datos (list): Lista de datos de inventario
        """
        total = len(datos)
        stock_bajo = sum(1 for item in datos if item['stock'] < item.get('stock_minimo', 0))
        
        self.label_total.setText(f"Total: {total} productos")
        self.label_stock_bajo.setText(f"⚠️ Stock bajo: {stock_bajo}")
        
    def filtrar_datos(self):
        """
        Filtra los datos según el texto de búsqueda y filtros activos.
        """
        if not hasattr(self, 'datos_originales'):
            return
            
        texto = self.search_input.text().lower()
        solo_stock_bajo = self.btn_stock_bajo.isChecked()
        
        # Filtrar datos
        datos_filtrados = []
        
        for item in self.datos_originales:
            # Filtro por stock bajo
            if solo_stock_bajo:
                if item['stock'] >= item.get('stock_minimo', 0):
                    continue
            
            # Filtro por texto de búsqueda
            if texto:
                id_producto = str(item.get('id_producto', '').lower())
                if texto not in id_producto:
                    continue
            
            datos_filtrados.append(item)
        
        # Mostrar datos filtrados
        self.mostrar_datos(datos_filtrados)
        self.actualizar_estadisticas(datos_filtrados)
        
    def toggle_stock_bajo(self):
        """
        Alterna el filtro de stock bajo.
        """
        self.filtrar_datos()
        
        # Cambiar texto del botón
        if self.btn_stock_bajo.isChecked():
            self.btn_stock_bajo.setText("📊 Ver Todo")
        else:
            self.btn_stock_bajo.setText("⚠️ Ver Stock Bajo")