# ==============================================================================
# ARCHIVO: views/tablas/empleado_view.py
# ==============================================================================
"""
Vista de Empleados.
Cada nodo solo ve sus empleados locales.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.consultas_quito import (
    obtener_empleados_quito,
    obtener_empleados_quito_por_tienda,
    eliminar_empleado_quito,
)
from database.consultas_loja import (
    obtener_empleados_loja,
    obtener_empleados_loja_por_tienda,
    eliminar_empleado_loja,
)
from views.formularios.empleado_form import EmpleadoForm


class EmpleadoView(QWidget):
    """Vista para gestionar Empleados locales."""
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.init_ui()
        self.cargar_datos()
        self.showMaximized()
        
    def init_ui(self):
        """Similar a cliente_view.py pero con columnas de empleados."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Título
        title = QLabel("Empleados")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2d3748;")
        layout.addWidget(title)
        
        # Búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar...")
        self.search_input.setFixedHeight(40)
        self.search_input.textChanged.connect(self.filtrar_datos)
        layout.addWidget(self.search_input)
        
        # Botones
        buttons_layout = QHBoxLayout()
        self.btn_nuevo = QPushButton("+ Nuevo")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_actualizar = QPushButton("🔄 Actualizar")
        
        self.btn_editar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        
        self.btn_nuevo.clicked.connect(self.nuevo_registro)
        self.btn_editar.clicked.connect(self.editar_registro)
        self.btn_eliminar.clicked.connect(self.eliminar_registro)
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        
        buttons_layout.addWidget(self.btn_nuevo)
        buttons_layout.addWidget(self.btn_editar)
        buttons_layout.addWidget(self.btn_eliminar)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_actualizar)
        layout.addLayout(buttons_layout)
        
        # Tabla
        self.tabla = QTableWidget()
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Nombre', 'Teléfono', 'Cargo', 'Fecha Contratación'])
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.itemSelectionChanged.connect(self.on_selection_changed)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)
        
        self.info_label = QLabel("Mostrando 0 registros")
        layout.addWidget(self.info_label)
        
    def cargar_datos(self):
        if self.nodo == 'gestion':
            # Mostrar solo empleados de la sucursal activa (Quito). Usamos tienda 1 por ahora.
            empleados = obtener_empleados_quito_por_tienda(1)
        else:
            # Loja: solo empleados de la sucursal 3
            empleados = obtener_empleados_loja_por_tienda(3)
        
        # Ordenar por ID
        empleados_ordenados = sorted(empleados, key=lambda x: x['id'])

        self.datos_originales = empleados_ordenados
        self.mostrar_datos(empleados_ordenados)

        
    def mostrar_datos(self, datos):
        self.tabla.setRowCount(0)
        for emp in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(emp['id'])))
            self.tabla.setItem(row, 1, QTableWidgetItem(emp['nombre']))
            self.tabla.setItem(row, 2, QTableWidgetItem(emp['telefono']))
            self.tabla.setItem(row, 3, QTableWidgetItem(emp['cargo']))
            fecha = emp['fecha_contratacion'].split(' ')[0] if emp['fecha_contratacion'] else ''
            self.tabla.setItem(row, 4, QTableWidgetItem(fecha))
        self.info_label.setText(f"Mostrando {len(datos)} registros")
        
    def filtrar_datos(self):
        if not hasattr(self, 'datos_originales'):
            return
        texto = self.search_input.text().lower()
        if not texto:
            self.mostrar_datos(self.datos_originales)
            return
        datos_filtrados = [e for e in self.datos_originales if texto in e['nombre'].lower() or texto in e['cargo'].lower()]
        self.mostrar_datos(datos_filtrados)
        
    def on_selection_changed(self):
        hay = len(self.tabla.selectedItems()) > 0
        self.btn_editar.setEnabled(hay)
        self.btn_eliminar.setEnabled(hay)
        
    def nuevo_registro(self):
        form = EmpleadoForm(self.datos_usuario, modo='nuevo')
        if form.exec_():
            self.cargar_datos()
            
    def editar_registro(self):
        row = self.tabla.currentRow()
        if row < 0:
            return
        datos = {
            'id': int(self.tabla.item(row, 0).text()),
            'nombre': self.tabla.item(row, 1).text(),
            'telefono': self.tabla.item(row, 2).text(),
            'cargo': self.tabla.item(row, 3).text()
        }
        form = EmpleadoForm(self.datos_usuario, modo='editar', datos=datos)
        if form.exec_():
            self.cargar_datos()
            
    def eliminar_registro(self):
        row = self.tabla.currentRow()
        if row < 0:
            return
        id_emp = int(self.tabla.item(row, 0).text())
        nombre = self.tabla.item(row, 1).text()
        resp = QMessageBox.question(self, "Confirmar", f"¿Eliminar empleado '{nombre}'?", QMessageBox.Yes | QMessageBox.No)
        if resp == QMessageBox.Yes:
            if self.nodo == 'gestion':
                ok = eliminar_empleado_quito(id_emp)
            else:
                ok = eliminar_empleado_loja(id_emp)
            if ok:
                QMessageBox.information(self, "Éxito", "Empleado eliminado")
                self.cargar_datos()

