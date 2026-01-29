
# ==============================================================================
# ARCHIVO: views/tablas/venta_view.py
# ==============================================================================
"""
Vista de Ventas.
Cada nodo solo ve sus ventas locales.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QLabel,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.consultas_quito import obtener_ventas_quito, eliminar_venta_quito
from database.consultas_loja import obtener_ventas_loja, eliminar_venta_loja
from views.formularios.venta_form import VentaForm, EditVentaForm


class VentaView(QWidget):
    """Vista para gestionar Ventas locales."""
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.init_ui()
        self.cargar_datos()
        self.showMaximized()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel("Ventas")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        layout.addWidget(title)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar...")
        self.search_input.setFixedHeight(40)
        layout.addWidget(self.search_input)
        
        buttons = QHBoxLayout()
        self.btn_nueva = QPushButton("+ Nueva Venta")
        self.btn_ver_detalle = QPushButton("Ver Detalle")
        self.btn_editar = QPushButton("Editar Venta")
        self.btn_eliminar = QPushButton("Eliminar Venta")
        self.btn_actualizar = QPushButton("🔄 Actualizar")
        
        self.btn_ver_detalle.setEnabled(False)
        self.btn_editar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        
        self.btn_nueva.clicked.connect(self.nueva_venta)
        self.btn_ver_detalle.clicked.connect(self.ver_detalle)
        self.btn_editar.clicked.connect(self.editar_venta)
        self.btn_eliminar.clicked.connect(self.eliminar_venta)
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        
        buttons.addWidget(self.btn_nueva)
        buttons.addWidget(self.btn_ver_detalle)
        buttons.addWidget(self.btn_editar)
        buttons.addWidget(self.btn_eliminar)
        buttons.addStretch()
        buttons.addWidget(self.btn_actualizar)
        layout.addLayout(buttons)
        
        self.tabla = QTableWidget()
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Fecha', 'Cliente', 'Total', 'ID Empleado', 'ID Tienda'])
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.itemSelectionChanged.connect(self.on_selection_changed)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        
        self.info_label = QLabel("Mostrando 0 registros")
        layout.addWidget(self.info_label)
        
    def cargar_datos(self):
        if self.nodo == 'gestion':
            ventas = obtener_ventas_quito()
        else:
            ventas = obtener_ventas_loja()
        self.datos_originales = ventas
        self.mostrar_datos(ventas)
        
    def mostrar_datos(self, datos):
        self.tabla.setRowCount(0)
        for v in datos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(v['id'])))
            fecha = v['fecha'].split(' ')[0] if v['fecha'] else ''
            self.tabla.setItem(row, 1, QTableWidgetItem(fecha))
            self.tabla.setItem(row, 2, QTableWidgetItem(v['nombre_cliente']))
            self.tabla.setItem(row, 3, QTableWidgetItem(f"${v['total']:.2f}"))
            self.tabla.setItem(row, 4, QTableWidgetItem(str(v['id_empleado'])))
            self.tabla.setItem(row, 5, QTableWidgetItem(str(v['id_tienda'])))
        self.info_label.setText(f"Mostrando {len(datos)} registros")
        
    def on_selection_changed(self):
        has_sel = len(self.tabla.selectedItems()) > 0
        self.btn_ver_detalle.setEnabled(has_sel)
        self.btn_editar.setEnabled(has_sel)
        self.btn_eliminar.setEnabled(has_sel)
        
    def nueva_venta(self):
        form = VentaForm(self.datos_usuario)
        if form.exec_():
            self.cargar_datos()
            
    def ver_detalle(self):
        row = self.tabla.currentRow()
        if row < 0:
            return
        id_venta = int(self.tabla.item(row, 0).text())
        fecha = self.tabla.item(row, 1).text()
        cliente = self.tabla.item(row, 2).text()
        total = self.tabla.item(row, 3).text()

        # Importar aquí para evitar circular
        from views.tablas.detalle_venta_view import DetalleVentaDialog
        dialog = DetalleVentaDialog(self.datos_usuario, id_venta, fecha, cliente, total)
        dialog.exec_()

    def editar_venta(self):
        row = self.tabla.currentRow()
        if row < 0:
            return
        id_venta = int(self.tabla.item(row, 0).text())
        form = EditVentaForm(self.datos_usuario, id_venta)
        if form.exec_():
            self.cargar_datos()

    def eliminar_venta(self):
        row = self.tabla.currentRow()
        if row < 0:
            return
        id_venta = int(self.tabla.item(row, 0).text())
        resp = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Eliminar la venta #{id_venta}? Esto revertirá el stock.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if resp != QMessageBox.Yes:
            return
        ok = eliminar_venta_quito(id_venta) if self.nodo == 'gestion' else eliminar_venta_loja(id_venta)
        if ok:
            QMessageBox.information(self, "Éxito", f"Venta #{id_venta} eliminada")
            self.cargar_datos()
        else:
            QMessageBox.critical(self, "Error", "No se pudo eliminar la venta")
