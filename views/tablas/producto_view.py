"""
views/tablas/producto_view.py
==============================
Vista de gestión de Productos.

PERMISOS:
- Quito: CRUD completo
- Loja: SOLO LECTURA (no puede crear/editar/eliminar)

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
                             QHeaderView, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.consultas_quito import (obtener_productos_quito, eliminar_producto_quito)
from database.consultas_loja import obtener_productos_loja
from views.formularios.producto_form import ProductoForm


class ProductoView(QWidget):
    """
    Vista para gestionar Productos.
    Quito: CRUD completo
    Loja: SOLO LECTURA
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.solo_lectura = (self.nodo == 'operacion')  # Loja es solo lectura
        self.init_ui()
        self.cargar_datos()
        self.showMaximized()
        
    def init_ui(self):
        """
        Inicializa la interfaz de usuario.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # ==================== ENCABEZADO ====================
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Productos")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2d3748;")
        
        header_layout.addWidget(title_label)
        
        # Indicador de solo lectura
        if self.solo_lectura:
            readonly_label = QLabel("👁️ Solo Lectura")
            readonly_label.setFont(QFont("Segoe UI", 12))
            readonly_label.setStyleSheet("""
                background-color: #fef3c7;
                color: #92400e;
                padding: 5px 15px;
                border-radius: 12px;
                font-weight: bold;
            """)
            header_layout.addWidget(readonly_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # ==================== BARRA DE BÚSQUEDA Y FILTROS ====================
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar...")
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
        
        # Filtro por categoría
        self.filtro_categoria = QComboBox()
        self.filtro_categoria.addItems(["- Todas las categorías -"])
        self.filtro_categoria.setFixedHeight(40)
        self.filtro_categoria.setFixedWidth(200)
        self.filtro_categoria.setStyleSheet("""
            QComboBox {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
                background-color: white;
            }
        """)
        self.filtro_categoria.currentTextChanged.connect(self.filtrar_datos)
        
        label_filtro = QLabel("Categoría:")
        label_filtro.setStyleSheet("color: #718096; font-size: 14px;")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(label_filtro)
        search_layout.addWidget(self.filtro_categoria)
        
        layout.addLayout(search_layout)
        
        # ==================== BOTONES DE ACCIÓN ====================
        buttons_layout = QHBoxLayout()
        
        # Los botones de modificación solo están disponibles para Quito
        if not self.solo_lectura:
            self.btn_nuevo = QPushButton("+ Nuevo")
            self.btn_nuevo.setFixedHeight(40)
            self.btn_nuevo.setCursor(Qt.PointingHandCursor)
            self.btn_nuevo.setStyleSheet("""
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
            self.btn_nuevo.clicked.connect(self.nuevo_registro)
            
            self.btn_editar = QPushButton("Editar")
            self.btn_editar.setFixedHeight(40)
            self.btn_editar.setCursor(Qt.PointingHandCursor)
            self.btn_editar.setEnabled(False)
            self.btn_editar.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #3d5a80;
                    border: 2px solid #3d5a80;
                    border-radius: 8px;
                    padding: 0 20px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover:enabled {
                    background-color: #f7fafc;
                }
                QPushButton:disabled {
                    opacity: 0.5;
                }
            """)
            self.btn_editar.clicked.connect(self.editar_registro)
            
            self.btn_eliminar = QPushButton("Eliminar")
            self.btn_eliminar.setFixedHeight(40)
            self.btn_eliminar.setCursor(Qt.PointingHandCursor)
            self.btn_eliminar.setEnabled(False)
            self.btn_eliminar.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #e53e3e;
                    border: 2px solid #e53e3e;
                    border-radius: 8px;
                    padding: 0 20px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover:enabled {
                    background-color: #fff5f5;
                }
                QPushButton:disabled {
                    opacity: 0.5;
                }
            """)
            self.btn_eliminar.clicked.connect(self.eliminar_registro)
            
            buttons_layout.addWidget(self.btn_nuevo)
            buttons_layout.addWidget(self.btn_editar)
            buttons_layout.addWidget(self.btn_eliminar)
        
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
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_actualizar)
        
        layout.addLayout(buttons_layout)
        
        # ==================== TABLA ====================
        self.tabla = QTableWidget()
        self.tabla.verticalHeader().setVisible(False)
        if self.nodo == 'gestion':
            self.tabla.setColumnCount(10)
            self.tabla.setHorizontalHeaderLabels([
                'ID', 'Nombre', 'Marca', 'Modelo', 'Categoría',
                'Precio', 'Stock Mín',
                'Costo Logístico', 'Margen %', 'Clasificación'
            ])
        else:
            self.tabla.setColumnCount(7)
            self.tabla.setHorizontalHeaderLabels([
                'ID', 'Nombre', 'Marca', 'Modelo',
                'Categoría', 'Precio', 'Stock Mín'
            ])

        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        if self.nodo == 'gestion':
            header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(9, QHeaderView.ResizeToContents)

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
        
        if not self.solo_lectura:
            self.tabla.itemSelectionChanged.connect(self.on_selection_changed)
            
        layout.addWidget(self.tabla)
        
        # ==================== INFORMACIÓN ====================
        self.info_label = QLabel("Mostrando 0 registros")
        self.info_label.setStyleSheet("color: #718096; font-size: 13px; padding: 10px 0;")
        layout.addWidget(self.info_label)
        
    def cargar_datos(self):
        """
        Carga los datos de productos desde la base de datos según el nodo.
        """
        try:
            if self.nodo == 'gestion':
                productos = obtener_productos_quito()
            else:
                productos = obtener_productos_loja()
            
            # ORDENAR por ID de producto
            productos_ordenados = sorted(productos, key=lambda x: x['id'])

            self.datos_originales = productos_ordenados

            # Obtener categorías únicas para el filtro
            categorias = set(p['categoria'] for p in productos_ordenados if p['categoria'])
            self.filtro_categoria.clear()
            self.filtro_categoria.addItem("- Todas las categorías -")
            self.filtro_categoria.addItems(sorted(categorias))

            self.mostrar_datos(productos_ordenados)

            
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
            
    def mostrar_datos(self, datos):
        """
        Muestra los datos en la tabla.
        """
        self.tabla.setRowCount(0)
        
        for producto in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            self.tabla.setItem(row, 0, QTableWidgetItem(str(producto['id'])))
            self.tabla.setItem(row, 1, QTableWidgetItem(producto['nombre']))
            self.tabla.setItem(row, 2, QTableWidgetItem(producto['marca']))
            self.tabla.setItem(row, 3, QTableWidgetItem(producto['modelo']))
            self.tabla.setItem(row, 4, QTableWidgetItem(producto['categoria']))
            self.tabla.setItem(row, 5, QTableWidgetItem(f"${producto['precio']:.2f}"))
            self.tabla.setItem(row, 6, QTableWidgetItem(str(producto['stock_minimo'])))
            if self.nodo == 'gestion':
                self.tabla.setItem(row, 7, QTableWidgetItem(f"${producto['costo_logistico']:.2f}"))
                self.tabla.setItem(row, 8, QTableWidgetItem(f"{producto['margen_porcentaje']:.2f} %"))
                self.tabla.setItem(row, 9, QTableWidgetItem(producto['clasificacion_planeacion']))
        self.info_label.setText(f"Mostrando {len(datos)} registros")
        
    def filtrar_datos(self):
        """
        Filtra los datos según el texto de búsqueda y categoría.
        """
        if not hasattr(self, 'datos_originales'):
            return
            
        texto = self.search_input.text().lower()
        categoria = self.filtro_categoria.currentText()
        
        datos_filtrados = []
        
        for producto in self.datos_originales:
            # Filtro por categoría
            if categoria != "- Todas las categorías -" and producto['categoria'] != categoria:
                continue
                
            # Filtro por texto
            if texto:
                if (texto not in producto['nombre'].lower() and
                    texto not in producto['marca'].lower() and
                    texto not in producto['modelo'].lower()):
                    continue
            
            datos_filtrados.append(producto)
        
        self.mostrar_datos(datos_filtrados)
        
    def on_selection_changed(self):
        """
        Maneja el cambio de selección en la tabla.
        """
        if self.solo_lectura:
            return
            
        hay_seleccion = len(self.tabla.selectedItems()) > 0
        self.btn_editar.setEnabled(hay_seleccion)
        self.btn_eliminar.setEnabled(hay_seleccion)
        
    def nuevo_registro(self):
        """
        Abre el formulario para crear un nuevo producto.
        Solo disponible para Quito.
        """
        if self.solo_lectura:
            return
            
        form = ProductoForm(self.datos_usuario, modo='nuevo')
        if form.exec_():
            self.cargar_datos()
            
    def editar_registro(self):
        """
        Abre el formulario para editar el producto seleccionado.
        Solo disponible para Quito.
        """
        if self.solo_lectura:
            return
            
        row = self.tabla.currentRow()
        if row < 0:
            return
            
        datos = {
            'id': int(self.tabla.item(row, 0).text()),
            'nombre': self.tabla.item(row, 1).text(),
            'marca': self.tabla.item(row, 2).text(),
            'modelo': self.tabla.item(row, 3).text(),
            'categoria': self.tabla.item(row, 4).text(),
            'precio': float(self.tabla.item(row, 5).text().replace('$', '')),
            'stock_minimo': int(self.tabla.item(row, 6).text())
        }
        
        form = ProductoForm(self.datos_usuario, modo='editar', datos=datos)
        if form.exec_():
            self.cargar_datos()
            
    def eliminar_registro(self):
        """
        Elimina el producto seleccionado.
        Solo disponible para Quito.
        """
        if self.solo_lectura:
            return
            
        row = self.tabla.currentRow()
        if row < 0:
            return
            
        id_producto = int(self.tabla.item(row, 0).text())
        nombre = self.tabla.item(row, 1).text()
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el producto '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            if eliminar_producto_quito(id_producto):
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                self.cargar_datos()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el producto")