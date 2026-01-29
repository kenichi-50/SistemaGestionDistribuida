# ==============================================================================
# ARCHIVO: views/formularios/venta_form.py
# ==============================================================================
"""Formulario para registrar una nueva venta."""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QComboBox, QSpinBox,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from database.consultas_quito import (
    obtener_clientes_quito,
    obtener_productos_quito_por_tienda,
    obtener_empleados_quito_por_tienda,
    insertar_venta_quito,
    obtener_venta_quito_por_id,
    actualizar_venta_quito,
    obtener_detalle_venta_quito
)
from database.consultas_loja import (
    obtener_clientes_loja,
    obtener_productos_loja_por_tienda,
    obtener_empleados_loja_por_tienda,
    insertar_venta_loja,
    obtener_venta_loja_por_id,
    actualizar_venta_loja,
    obtener_detalle_venta_loja
)


class VentaForm(QDialog):
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.nodo = datos_usuario['nodo']
        self.detalles = []
        self.productos_dict = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Nueva Venta")
        self.setFixedSize(700, 600)
        self.setModal(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)

        title = QLabel("Registrar Nueva Venta")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        # Cliente
        layout.addWidget(QLabel("Cliente"))
        self.combo_cliente = QComboBox()
        self.combo_cliente.setFixedHeight(40)
        layout.addWidget(self.combo_cliente)
        self.cargar_clientes()

        # Empleado
        layout.addWidget(QLabel("Empleado"))
        self.combo_empleado = QComboBox()
        self.combo_empleado.setFixedHeight(40)
        layout.addWidget(self.combo_empleado)
        self.cargar_empleados()

        # Agregar productos
        layout.addWidget(QLabel("Agregar Productos"))
        row_producto = QHBoxLayout()

        self.combo_producto = QComboBox()
        self.combo_producto.setFixedWidth(300)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 999)
        self.spin_cantidad.setValue(1)

        self.btn_agregar = QPushButton("+ Agregar")
        self.btn_agregar.clicked.connect(self.agregar_producto)

        row_producto.addWidget(self.combo_producto)
        row_producto.addWidget(QLabel("Cant:"))
        row_producto.addWidget(self.spin_cantidad)
        row_producto.addWidget(self.btn_agregar)
        layout.addLayout(row_producto)

        # Tabla de productos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(['Producto', 'Cantidad', 'P. Unit', 'Subtotal', ''])
        layout.addWidget(self.tabla)

        # Total
        self.label_total = QLabel("Total: $0.00")
        self.label_total.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(self.label_total)

        # Botones
        buttons = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Registrar Venta")
        btn_guardar.setStyleSheet("background-color: #3d5a80; color: white; font-weight: bold;")
        btn_guardar.clicked.connect(self.guardar)

        buttons.addWidget(btn_cancelar)
        buttons.addWidget(btn_guardar)
        layout.addLayout(buttons)

        # Eventos y datos
        self.combo_producto.currentIndexChanged.connect(self.actualizar_max_cantidad)
        self.cargar_productos()
        self.actualizar_max_cantidad()

    def cargar_clientes(self):
        clientes = obtener_clientes_quito() if self.nodo == 'gestion' else obtener_clientes_loja()
        for c in clientes:
            self.combo_cliente.addItem(c['nombre'], c['id'])

    def cargar_empleados(self):
        if self.nodo == 'gestion':
            # Quito: mostrar únicamente empleados de la sucursal activa (usar 1 por ahora)
            empleados = obtener_empleados_quito_por_tienda(1)
        else:
            empleados = obtener_empleados_loja_por_tienda(3)
        for e in empleados:
            self.combo_empleado.addItem(e['nombre'], e['id'])

    def cargar_productos(self):
        if self.nodo == 'gestion':
            productos = obtener_productos_quito_por_tienda(1)
        else:
            productos = obtener_productos_loja_por_tienda(3)
        self.combo_producto.clear()
        self.productos_dict = {p['id']: p for p in productos}
        for p in productos:
            self.combo_producto.addItem(f"{p['nombre']} - ${p['precio']:.2f}", p['id'])

    def agregar_producto(self):
        id_producto = self.combo_producto.currentData()
        cantidad = self.spin_cantidad.value()
        if not id_producto:
            return
        producto = self.productos_dict.get(id_producto)
        if not producto:
            return
        # Validar stock disponible en Quito
        disponible = self._stock_disponible(id_producto)
        if disponible <= 0:
            QMessageBox.warning(self, "Sin stock", "No hay stock disponible para este producto en la sucursal.")
            return
        if cantidad > disponible:
            QMessageBox.warning(self, "Cantidad excedida", f"Solo hay {disponible} unidades disponibles.")
            return
        self.detalles.append({
            'id_producto': id_producto,
            'nombre': producto['nombre'],
            'cantidad': cantidad,
            'precio_unitario': producto.get('precio', 0.0)
        })
        self.actualizar_tabla()
        self.actualizar_max_cantidad()

    def actualizar_tabla(self):
        self.tabla.setRowCount(0)
        total = 0
        for det in self.detalles:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            subtotal = det['cantidad'] * det['precio_unitario']
            total += subtotal

            self.tabla.setItem(row, 0, QTableWidgetItem(det['nombre']))
            self.tabla.setItem(row, 1, QTableWidgetItem(str(det['cantidad'])))
            self.tabla.setItem(row, 2, QTableWidgetItem(f"${det['precio_unitario']:.2f}"))
            self.tabla.setItem(row, 3, QTableWidgetItem(f"${subtotal:.2f}"))

            btn_eliminar = QPushButton("X")
            btn_eliminar.clicked.connect(lambda checked, r=row: self.eliminar_detalle(r))
            self.tabla.setCellWidget(row, 4, btn_eliminar)

        self.label_total.setText(f"Total: ${total:.2f}")

    def eliminar_detalle(self, row):
        if 0 <= row < len(self.detalles):
            self.detalles.pop(row)
            self.actualizar_tabla()
            self.actualizar_max_cantidad()

    def _cantidad_seleccionada_actual(self, id_producto):
        return sum(d['cantidad'] for d in self.detalles if d['id_producto'] == id_producto)

    def _stock_disponible(self, id_producto):
        p = self.productos_dict.get(id_producto)
        stock = p.get('stock') if p else None
        if stock is None:
            # Para Loja o si no viene stock, no limitar aquí
            return 999
        usado = self._cantidad_seleccionada_actual(id_producto)
        restante = max(0, stock - usado)
        return restante

    def actualizar_max_cantidad(self):
        id_producto = self.combo_producto.currentData()
        if not id_producto:
            return
        restante = self._stock_disponible(id_producto)
        if restante <= 0:
            self.spin_cantidad.setRange(0, 0)
            self.spin_cantidad.setValue(0)
            self.btn_agregar.setEnabled(False)
        else:
            self.spin_cantidad.setRange(1, restante)
            if self.spin_cantidad.value() > restante:
                self.spin_cantidad.setValue(restante)
            self.btn_agregar.setEnabled(True)

    def guardar(self):
        if self.combo_cliente.count() == 0:
            QMessageBox.warning(self, "Error", "No hay clientes disponibles. Registre un cliente primero.")
            return
        if self.combo_empleado.count() == 0:
            QMessageBox.warning(self, "Error", "No hay empleados en la sucursal seleccionada.")
            return
        if not self.detalles:
            QMessageBox.warning(self, "Error", "Debe agregar al menos un producto")
            return
        # Validación final: total por producto no debe exceder stock (Quito y Loja)
        totales = {}
        for d in self.detalles:
            totales[d['id_producto']] = totales.get(d['id_producto'], 0) + d['cantidad']
        for pid, total in totales.items():
            stock = self.productos_dict.get(pid, {}).get('stock')
            if stock is not None and total > stock:
                QMessageBox.critical(self, "Stock insuficiente", "La cantidad agregada excede el stock disponible en sucursal.")
                return

        id_cliente = self.combo_cliente.currentData()
        id_empleado = self.combo_empleado.currentData()
        id_tienda = 1 if self.nodo == 'gestion' else 3

        try:
            if self.nodo == 'gestion':
                id_venta = insertar_venta_quito(id_cliente, id_empleado, id_tienda, self.detalles)
            else:
                id_venta = insertar_venta_loja(id_cliente, id_empleado, id_tienda, self.detalles)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar la venta:\n{str(e)}")
            return

        if id_venta:
            QMessageBox.information(self, "Éxito", f"Venta #{id_venta} registrada correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la venta. Verifique stock disponible, cliente y empleado válidos.")


class EditVentaForm(VentaForm):
    def __init__(self, datos_usuario, id_venta):
        self.id_venta = id_venta
        super().__init__(datos_usuario)

    def init_ui(self):
        super().init_ui()
        self.setWindowTitle("Editar Venta")
        # Cambiar texto del botón guardar
        # Buscar el botón en el layout final
        # Asumimos que el último layout tiene dos botones, reemplazamos conexión
        # Nota: mantenemos estilo original
        # Reasignar handler de guardar
        # No cambiamos el texto para evitar buscar el widget; manejamos por acción

        # Prefill datos
        self._prefill_datos()

    def _prefill_datos(self):
        # Obtener cabecera y detalles
        if self.nodo == 'gestion':
            venta = obtener_venta_quito_por_id(self.id_venta)
            detalles = obtener_detalle_venta_quito(self.id_venta)
        else:
            venta = obtener_venta_loja_por_id(self.id_venta)
            detalles = obtener_detalle_venta_loja(self.id_venta)
        if not venta:
            QMessageBox.critical(self, "Error", "No se pudo cargar la venta")
            return
        # Seleccionar cliente
        idx_cliente = self.combo_cliente.findData(venta['id_cliente'])
        if idx_cliente >= 0:
            self.combo_cliente.setCurrentIndex(idx_cliente)
        # Seleccionar empleado
        idx_empleado = self.combo_empleado.findData(venta['id_empleado'])
        if idx_empleado >= 0:
            self.combo_empleado.setCurrentIndex(idx_empleado)
        # Construir detalles
        self.detalles = []
        for d in detalles:
            self.detalles.append({
                'id_producto': d['id_producto'],
                'nombre': d['nombre_producto'],
                'cantidad': d.get('cantidad', 1),
                'precio_unitario': d.get('precio_unitario', 0.0)
            })
        self.actualizar_tabla()

    def guardar(self):
        if not self.detalles:
            QMessageBox.warning(self, "Error", "Debe agregar al menos un producto")
            return
        # Validación de stock igual que en alta
        totales = {}
        for d in self.detalles:
            totales[d['id_producto']] = totales.get(d['id_producto'], 0) + d['cantidad']
        for pid, total in totales.items():
            stock = self.productos_dict.get(pid, {}).get('stock')
            if stock is not None and total > stock:
                QMessageBox.critical(self, "Stock insuficiente", "La cantidad agregada excede el stock disponible en sucursal.")
                return

        id_cliente = self.combo_cliente.currentData()
        id_empleado = self.combo_empleado.currentData()

        if self.nodo == 'gestion':
            ok = actualizar_venta_quito(self.id_venta, id_cliente, id_empleado, self.detalles)
        else:
            ok = actualizar_venta_loja(self.id_venta, id_cliente, id_empleado, self.detalles)

        if ok:
            QMessageBox.information(self, "Éxito", f"Venta #{self.id_venta} actualizada correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar la venta")