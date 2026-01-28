"""
views/tablas/tienda_view.py
============================
Vista de gestión de Tiendas.

IMPORTANTE: Solo disponible para Nodo de Gestión (Quito)
Loja NO tiene acceso a este módulo.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
                             QHeaderView, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.consultas_quito import (obtener_tiendas_quito, eliminar_tienda_quito)
from views.formularios.tienda_form import TiendaForm


class TiendaView(QWidget):
    """
    Vista para gestionar Tiendas.
    Solo Quito puede gestionar tiendas.
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
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
        
        # Título
        title_label = QLabel("Tiendas")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2d3748;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # ==================== BARRA DE BÚSQUEDA Y FILTROS ====================
        search_layout = QHBoxLayout()
        
        # Campo de búsqueda
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
        
        # Filtro por ciudad
        self.filtro_ciudad = QComboBox()
        self.filtro_ciudad.addItems(["- Seleccionar -", "Quito", "Loja", "Otra"])
        self.filtro_ciudad.setFixedHeight(40)
        self.filtro_ciudad.setFixedWidth(150)
        self.filtro_ciudad.setStyleSheet("""
            QComboBox {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
                background-color: white;
            }
        """)
        self.filtro_ciudad.currentTextChanged.connect(self.filtrar_datos)
        
        label_filtro = QLabel("Filtrar por:")
        label_filtro.setStyleSheet("color: #718096; font-size: 14px;")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(label_filtro)
        search_layout.addWidget(self.filtro_ciudad)
        
        layout.addLayout(search_layout)
        
        # ==================== BOTONES DE ACCIÓN ====================
        buttons_layout = QHBoxLayout()
        
        # Botón Nuevo
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
        
        # Botón Editar
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
        
        # Botón Eliminar
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
        
        # Botón Actualizar
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
        
        buttons_layout.addWidget(self.btn_nuevo)
        buttons_layout.addWidget(self.btn_editar)
        buttons_layout.addWidget(self.btn_eliminar)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_actualizar)
        
        layout.addLayout(buttons_layout)
        
        # ==================== TABLA ====================
        self.tabla = QTableWidget()
        self.tabla.verticalHeader().setVisible(False)

        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Nombre', 'Ciudad', 'Dirección', 'Teléfono'])
        
        # Configurar tabla
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Ajustar columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
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
                border-bottom: 1px solid #f7fafc;
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
        
        # Conectar evento de selección
        self.tabla.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.tabla)
        
        # ==================== INFORMACIÓN ====================
        self.info_label = QLabel("Mostrando 0 registros")
        self.info_label.setStyleSheet("color: #718096; font-size: 13px; padding: 10px 0;")
        layout.addWidget(self.info_label)
        
    def cargar_datos(self):
        """
        Carga los datos de tiendas desde la base de datos.
        """
        try:
            # Obtener tiendas desde Quito
            tiendas = obtener_tiendas_quito()

            # 🔽 ORDENAR POR ID
            tiendas_ordenadas = sorted(tiendas, key=lambda x: x['id'])

            self.datos_originales = tiendas_ordenadas
            self.mostrar_datos(tiendas_ordenadas)
            
        except Exception as e:
            print(f"Error al cargar tiendas: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
            
    def mostrar_datos(self, datos):
        """
        Muestra los datos en la tabla.
        
        Args:
            datos (list): Lista de diccionarios con datos de tiendas
        """
        self.tabla.setRowCount(0)
        
        for tienda in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            self.tabla.setItem(row, 0, QTableWidgetItem(str(tienda['id'])))
            self.tabla.setItem(row, 1, QTableWidgetItem(tienda['nombre']))
            self.tabla.setItem(row, 2, QTableWidgetItem(tienda['ciudad']))
            self.tabla.setItem(row, 3, QTableWidgetItem(tienda['direccion']))
            self.tabla.setItem(row, 4, QTableWidgetItem(tienda['telefono']))
        
        # Actualizar info
        self.info_label.setText(f"Mostrando {len(datos)} registros")
        
    def filtrar_datos(self):
        """
        Filtra los datos según el texto de búsqueda y filtros.
        """
        if not hasattr(self, 'datos_originales'):
            return
            
        texto_busqueda = self.search_input.text().lower()
        ciudad_filtro = self.filtro_ciudad.currentText()
        
        datos_filtrados = []
        
        for tienda in self.datos_originales:
            # Filtro por ciudad
            if ciudad_filtro != "- Seleccionar -" and tienda['ciudad'] != ciudad_filtro:
                continue
                
            # Filtro por texto de búsqueda
            if texto_busqueda:
                if (texto_busqueda not in tienda['nombre'].lower() and
                    texto_busqueda not in tienda['ciudad'].lower() and
                    texto_busqueda not in tienda['direccion'].lower()):
                    continue
            
            datos_filtrados.append(tienda)
        
        self.mostrar_datos(datos_filtrados)
        
    def on_selection_changed(self):
        """
        Maneja el cambio de selección en la tabla.
        """
        hay_seleccion = len(self.tabla.selectedItems()) > 0
        self.btn_editar.setEnabled(hay_seleccion)
        self.btn_eliminar.setEnabled(hay_seleccion)
        
    def nuevo_registro(self):
        """
        Abre el formulario para crear una nueva tienda.
        """
        form = TiendaForm(self.datos_usuario, modo='nuevo')
        if form.exec_():
            self.cargar_datos()
            
    def editar_registro(self):
        """
        Abre el formulario para editar la tienda seleccionada.
        """
        row = self.tabla.currentRow()
        if row < 0:
            return
            
        # Obtener datos de la fila
        datos = {
            'id': int(self.tabla.item(row, 0).text()),
            'nombre': self.tabla.item(row, 1).text(),
            'ciudad': self.tabla.item(row, 2).text(),
            'direccion': self.tabla.item(row, 3).text(),
            'telefono': self.tabla.item(row, 4).text()
        }
        
        form = TiendaForm(self.datos_usuario, modo='editar', datos=datos)
        if form.exec_():
            self.cargar_datos()
            
    def eliminar_registro(self):
        """
        Elimina la tienda seleccionada.
        """
        row = self.tabla.currentRow()
        if row < 0:
            return
            
        id_tienda = int(self.tabla.item(row, 0).text())
        nombre = self.tabla.item(row, 1).text()
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar la tienda '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            if eliminar_tienda_quito(id_tienda):
                QMessageBox.information(self, "Éxito", "Tienda eliminada correctamente")
                self.cargar_datos()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la tienda")