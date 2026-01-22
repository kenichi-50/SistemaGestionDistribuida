"""
views/tablas/cliente_view.py
=============================
Vista de gestión de clientes con conexión SQL Server.

NODO LOJA: CRUD completo de clientes
Los clientes son compartidos entre nodos.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QPushButton, QFrame,
                             QLineEdit, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from database.conexion import (obtener_clientes_loja, insertar_cliente_loja,
                               actualizar_cliente_loja, eliminar_cliente_loja)
from views.formularios.cliente_form import ClienteForm


class ClienteView(QMainWindow):
    """Vista de gestión de clientes con SQL Server."""
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.clientes = []
        self.cliente_form = None
        self.inicializar_ui()
        self.cargar_datos()
        
    def inicializar_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("Gestión de Clientes - Nodo Loja")
        self.setMinimumSize(1000, 600)
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        widget_central.setLayout(layout_principal)
        
        # Barra superior
        self.crear_barra_superior(layout_principal)
        
        # Área de contenido
        self.crear_area_contenido(layout_principal)
        
    def crear_barra_superior(self, layout_padre):
        """Crea la barra superior."""
        barra = QFrame()
        barra.setFixedHeight(70)
        barra.setStyleSheet("background-color: white; border-bottom: 1px solid #dcdde1;")
        
        layout_barra = QHBoxLayout()
        layout_barra.setContentsMargins(30, 15, 30, 15)
        barra.setLayout(layout_barra)
        
        # Breadcrumb
        breadcrumb = QLabel(f"Sistema de Gestión Distribuida > Nodo: {self.datos_usuario['ciudad']} > Clientes")
        breadcrumb.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        
        layout_barra.addWidget(breadcrumb)
        layout_barra.addStretch()
        
        # Usuario
        label_usuario = QLabel(f"👤 {self.datos_usuario['usuario']}")
        label_usuario.setStyleSheet("font-size: 14px; color: #2c3e50; margin-right: 15px;")
        
        # Botón cerrar
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
        """Crea el área de contenido."""
        frame_contenido = QFrame()
        frame_contenido.setStyleSheet("background-color: #ecf0f1;")
        
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(40, 30, 40, 30)
        layout_contenido.setSpacing(20)
        frame_contenido.setLayout(layout_contenido)
        
        # Título
        label_titulo = QLabel("Gestión de Clientes")
        label_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout_contenido.addWidget(label_titulo)
        
        # Barra de búsqueda y botones
        self.crear_barra_busqueda(layout_contenido)
        
        # Tabla
        self.crear_tabla(layout_contenido)
        
        layout_padre.addWidget(frame_contenido)
        
    def crear_barra_busqueda(self, layout_padre):
        """Crea la barra de búsqueda con botones."""
        frame_busqueda = QFrame()
        frame_busqueda.setStyleSheet("background-color: transparent;")
        
        layout_busqueda = QHBoxLayout()
        layout_busqueda.setContentsMargins(0, 0, 0, 0)
        frame_busqueda.setLayout(layout_busqueda)
        
        # Campo de búsqueda
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("🔍 Buscar cliente...")
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
        
        # Botón Nuevo
        btn_nuevo = QPushButton("+ Nuevo Cliente")
        btn_nuevo.setStyleSheet("""
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
        btn_nuevo.setCursor(Qt.PointingHandCursor)
        btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)
        
        # Botón Editar
        btn_editar = QPushButton("Editar")
        btn_editar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #ecf0f1; }
        """)
        btn_editar.setCursor(Qt.PointingHandCursor)
        btn_editar.clicked.connect(self.editar_seleccionado)
        
        # Botón Eliminar
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #ecf0f1; }
        """)
        btn_eliminar.setCursor(Qt.PointingHandCursor)
        btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        
        # Botón Actualizar
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #ecf0f1; }
        """)
        btn_actualizar.setCursor(Qt.PointingHandCursor)
        btn_actualizar.clicked.connect(self.cargar_datos)
        
        layout_busqueda.addWidget(btn_nuevo)
        layout_busqueda.addWidget(btn_editar)
        layout_busqueda.addWidget(btn_eliminar)
        layout_busqueda.addWidget(btn_actualizar)
        
        layout_padre.addWidget(frame_busqueda)
        
    def crear_tabla(self, layout_padre):
        """Crea la tabla de clientes."""
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Dirección", "Teléfono", "Correo", "Fecha Registro"
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
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        
        self.tabla.setColumnWidth(0, 60)
        self.tabla.setColumnWidth(3, 120)
        self.tabla.setColumnWidth(5, 120)
        
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)
        
        layout_padre.addWidget(self.tabla)
        
    def cargar_datos(self):
        """Carga los datos de clientes desde SQL Server."""
        print("\n🔄 Cargando clientes desde SQL Server...")
        self.clientes = obtener_clientes_loja()
        self.actualizar_tabla()
        print(f"✓ {len(self.clientes)} clientes cargados\n")
        
    def actualizar_tabla(self):
        """Actualiza la tabla con los clientes cargados."""
        self.tabla.setRowCount(0)
        
        for cliente in self.clientes:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            self.tabla.setItem(row, 0, QTableWidgetItem(str(cliente['id'])))
            self.tabla.setItem(row, 1, QTableWidgetItem(cliente['nombre']))
            self.tabla.setItem(row, 2, QTableWidgetItem(cliente.get('direccion', '')))
            self.tabla.setItem(row, 3, QTableWidgetItem(cliente.get('telefono', '')))
            self.tabla.setItem(row, 4, QTableWidgetItem(cliente.get('correo', '')))
            self.tabla.setItem(row, 5, QTableWidgetItem(cliente.get('fecha_registro', '')))
            
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
            
    def abrir_formulario_nuevo(self):
        """Abre el formulario para crear un nuevo cliente."""
        self.cliente_form = ClienteForm(self.datos_usuario)
        self.cliente_form.cliente_guardado.connect(self.cargar_datos)
        self.cliente_form.show()
        
    def editar_seleccionado(self):
        """Edita el cliente seleccionado."""
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada >= 0:
            cliente_id = int(self.tabla.item(fila_seleccionada, 0).text())
            cliente = next((c for c in self.clientes if c['id'] == cliente_id), None)
            
            if cliente:
                self.cliente_form = ClienteForm(self.datos_usuario, cliente)
                self.cliente_form.cliente_guardado.connect(self.cargar_datos)
                self.cliente_form.show()
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para editar")
            
    def eliminar_seleccionado(self):
        """Elimina el cliente seleccionado."""
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada >= 0:
            cliente_id = int(self.tabla.item(fila_seleccionada, 0).text())
            cliente_nombre = self.tabla.item(fila_seleccionada, 1).text()
            
            respuesta = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar al cliente '{cliente_nombre}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                if eliminar_cliente_loja(cliente_id):
                    QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                    self.cargar_datos()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo eliminar el cliente")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para eliminar")