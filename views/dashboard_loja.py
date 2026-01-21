"""
views/dashboard_operacion.py
=============================
Dashboard principal del Nodo de Operación (Loja).
Interfaz similar al dashboard de gestión pero sin módulo Tienda.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from views.tablas.producto_view import ProductoView
from views.tablas.cliente_view import ClienteView


class DashboardOperacion(QMainWindow):
    """
    Dashboard principal para el Nodo de Operación (Loja).
    
    ⚠️ SIN acceso al módulo Tienda
    Producto en modo SOLO LECTURA
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.ventana_activa = None
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Configura la interfaz del dashboard."""
        self.setWindowTitle("Sistema de Gestión Distribuida")
        self.setMinimumSize(1200, 700)
        self.showMaximized()
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        widget_central.setLayout(layout_principal)
        
        self.crear_sidebar(layout_principal)
        self.crear_area_contenido(layout_principal)
        
    def crear_sidebar(self, layout_padre):
        """Crea el sidebar SIN módulo Tienda."""
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("QFrame { background-color: #34495e; border: none; }")
        
        layout_sidebar = QVBoxLayout()
        layout_sidebar.setContentsMargins(0, 0, 0, 0)
        layout_sidebar.setSpacing(0)
        sidebar.setLayout(layout_sidebar)
        
        # Header
        header_sidebar = QFrame()
        header_sidebar.setStyleSheet("background-color: #2c3e50;")
        header_sidebar.setFixedHeight(70)
        
        layout_header = QVBoxLayout()
        layout_header.setContentsMargins(20, 15, 20, 15)
        header_sidebar.setLayout(layout_header)
        
        label_nodo = QLabel("Nodo de Operación")
        label_nodo.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        layout_header.addWidget(label_nodo)
        layout_sidebar.addWidget(header_sidebar)
        
        # ⚠️ IMPORTANTE: SIN módulo Tienda
        modulos = [
            ('👥', 'Cliente', self.abrir_clientes),
            ('📦', 'Producto', self.abrir_productos),  # Solo lectura
            ('👨‍💼', 'Empleado', self.abrir_empleados),
            ('🛒', 'Venta', self.abrir_ventas),
            ('📋', 'Detalle Venta', self.abrir_detalle_venta),
            ('📊', 'Inventario', self.abrir_inventario),
        ]
        
        for icono, nombre, funcion in modulos:
            btn = self.crear_boton_modulo(icono, nombre, funcion)
            layout_sidebar.addWidget(btn)
        
        layout_sidebar.addStretch()
        layout_padre.addWidget(sidebar)
        
    def crear_boton_modulo(self, icono, nombre, funcion):
        """Crea botón de módulo en sidebar."""
        btn = QPushButton(f"  {icono}  {nombre}")
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding: 15px 20px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1f618d; }
        """)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(funcion)
        return btn
        
    def crear_area_contenido(self, layout_padre):
        """Crea el área de contenido."""
        frame_contenido = QFrame()
        frame_contenido.setStyleSheet("background-color: #ecf0f1;")
        
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(0, 0, 0, 0)
        layout_contenido.setSpacing(0)
        frame_contenido.setLayout(layout_contenido)
        
        self.crear_barra_superior(layout_contenido)
        self.crear_area_bienvenida(layout_contenido)
        
        layout_padre.addWidget(frame_contenido)
        
    def crear_barra_superior(self, layout_padre):
        """Crea barra superior."""
        barra = QFrame()
        barra.setFixedHeight(70)
        barra.setStyleSheet("background-color: white; border-bottom: 1px solid #dcdde1;")
        
        layout_barra = QHBoxLayout()
        layout_barra.setContentsMargins(30, 15, 30, 15)
        barra.setLayout(layout_barra)
        
        label_nodo = QLabel("Nodo: Loja")
        label_nodo.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        layout_barra.addWidget(label_nodo)
        layout_barra.addStretch()
        
        label_usuario = QLabel(f"👤 {self.datos_usuario['usuario']}")
        label_usuario.setStyleSheet("font-size: 14px; color: #2c3e50; margin-right: 15px;")
        
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
        btn_cerrar.clicked.connect(self.cerrar_sesion)
        
        layout_barra.addWidget(label_usuario)
        layout_barra.addWidget(btn_cerrar)
        layout_padre.addWidget(barra)
        
    def crear_area_bienvenida(self, layout_padre):
        """Crea área de bienvenida con tarjetas."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        widget_scroll = QWidget()
        layout_scroll = QVBoxLayout()
        layout_scroll.setContentsMargins(40, 30, 40, 30)
        layout_scroll.setSpacing(20)
        widget_scroll.setLayout(layout_scroll)
        
        label_titulo = QLabel("Nodo de Operación")
        label_titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        
        label_subtitulo = QLabel(f"Bienvenido, {self.datos_usuario['usuario']}.")
        label_subtitulo.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        
        label_descripcion = QLabel("Desde aquí puedes consultar y gestionar cierta información del sistema distribuido.")
        label_descripcion.setStyleSheet("font-size: 13px; color: #95a5a6; margin-bottom: 20px;")
        
        layout_scroll.addWidget(label_titulo)
        layout_scroll.addWidget(label_subtitulo)
        layout_scroll.addWidget(label_descripcion)
        
        self.crear_grid_tarjetas(layout_scroll)
        
        label_footer = QLabel("© 2026 - Sistema Corporativo")
        label_footer.setAlignment(Qt.AlignCenter)
        label_footer.setStyleSheet("font-size: 11px; color: #95a5a6; margin-top: 30px;")
        
        layout_scroll.addStretch()
        layout_scroll.addWidget(label_footer)
        
        scroll.setWidget(widget_scroll)
        layout_padre.addWidget(scroll)
        
    def crear_grid_tarjetas(self, layout_padre):
        """Crea grid de tarjetas - CON tarjeta Producto deshabilitada."""
        frame_grid = QFrame()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        frame_grid.setLayout(grid_layout)
        
        # Tarjetas (Producto estará deshabilitado visualmente)
        tarjetas = [
            ('👥', 'Gestionar Clientes', 'Gestionar tiendas y\nsus ubicaciones.', self.abrir_clientes, True),
            ('📦', 'Ver Productos', 'Ver y administrar información\nproducto.', self.abrir_productos, True),
            ('👨‍💼', 'Gestionar Empleados', 'Gestionar Gestionar\nde Laopenceos.', self.abrir_empleados, True),
            ('🛒', 'Gestionar Ventas', 'Consultar y gestionar\nlas ventas y detalles.', self.abrir_ventas, True),
            ('📋', 'Gestionar Empleados', 'Gestionar Inventario\nde Loja.', self.abrir_detalle_venta, True),
        ]
        
        row, col = 0, 0
        for icono, titulo, descripcion, funcion, habilitado in tarjetas:
            tarjeta = self.crear_tarjeta(icono, titulo, descripcion, funcion, habilitado)
            grid_layout.addWidget(tarjeta, row, col)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        layout_padre.addWidget(frame_grid)
        
    def crear_tarjeta(self, icono, titulo, descripcion, funcion, habilitado=True):
        """Crea tarjeta de módulo."""
        tarjeta = QFrame()
        tarjeta.setFixedSize(280, 180)
        
        if habilitado:
            tarjeta.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 10px;
                    border: 1px solid #dcdde1;
                }
                QFrame:hover {
                    border: 1px solid #3498db;
                    background-color: #f8f9fa;
                }
            """)
            tarjeta.setCursor(Qt.PointingHandCursor)
        else:
            # Tarjeta deshabilitada
            tarjeta.setStyleSheet("""
                QFrame {
                    background-color: #f0f0f0;
                    border-radius: 10px;
                    border: 1px solid #dcdde1;
                    opacity: 0.5;
                }
            """)
        
        layout_tarjeta = QVBoxLayout()
        layout_tarjeta.setContentsMargins(20, 20, 20, 20)
        layout_tarjeta.setAlignment(Qt.AlignCenter)
        tarjeta.setLayout(layout_tarjeta)
        
        label_icono = QLabel(icono)
        label_icono.setStyleSheet("font-size: 48px;")
        label_icono.setAlignment(Qt.AlignCenter)
        
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("font-size: 15px; font-weight: bold; color: #2c3e50;")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setWordWrap(True)
        
        label_desc = QLabel(descripcion)
        label_desc.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        label_desc.setAlignment(Qt.AlignCenter)
        label_desc.setWordWrap(True)
        
        layout_tarjeta.addWidget(label_icono)
        layout_tarjeta.addSpacing(10)
        layout_tarjeta.addWidget(label_titulo)
        layout_tarjeta.addSpacing(5)
        layout_tarjeta.addWidget(label_desc)
        
        if habilitado:
            tarjeta.mousePressEvent = lambda event: funcion()
        
        return tarjeta
        
    # Funciones de navegación
    def abrir_clientes(self):
        if self.ventana_activa:
            self.ventana_activa.close()
        self.ventana_activa = ClienteView(self.datos_usuario)
        self.ventana_activa.show()
        
    def abrir_productos(self):
        if self.ventana_activa:
            self.ventana_activa.close()
        self.ventana_activa = ProductoView(self.datos_usuario)
        self.ventana_activa.show()
        
    def abrir_empleados(self):
        print("TODO: Abrir Empleados (filtrado por Loja)")
        
    def abrir_ventas(self):
        print("TODO: Abrir Ventas (filtrado por Loja)")
        
    def abrir_detalle_venta(self):
        print("TODO: Abrir Detalle Venta")
        
    def abrir_inventario(self):
        print("TODO: Abrir Inventario (filtrado por Loja)")
        
    def cerrar_sesion(self):
        from views.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()