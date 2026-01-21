"""
views/dashboard_gestion.py
===========================
Dashboard principal del Nodo de Gestión (Quito).
Interfaz basada en el diseño proporcionado.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.permisos import obtener_modulos_nodo
from views.tablas.producto_view import ProductoView
from views.tablas.cliente_view import ClienteView


class DashboardGestion(QMainWindow):
    """
    Dashboard principal para el Nodo de Gestión (Quito).
    
    Permite acceso completo a todos los módulos del sistema.
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.ventana_activa = None
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """
        Configura la interfaz del dashboard.
        """
        # Configuración de la ventana
        self.setWindowTitle("Sistema de Gestión Distribuida")
        self.setMinimumSize(1200, 700)
        self.showMaximized()
        
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal (horizontal: sidebar + contenido)
        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        widget_central.setLayout(layout_principal)
        
        # Crear sidebar
        self.crear_sidebar(layout_principal)
        
        # Crear área de contenido
        self.crear_area_contenido(layout_principal)
        
    def crear_sidebar(self, layout_padre):
        """
        Crea el menú lateral (sidebar) con los módulos disponibles.
        """
        # Frame del sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border: none;
            }
        """)
        
        # Layout del sidebar
        layout_sidebar = QVBoxLayout()
        layout_sidebar.setContentsMargins(0, 0, 0, 0)
        layout_sidebar.setSpacing(0)
        sidebar.setLayout(layout_sidebar)
        
        # ========== ENCABEZADO DEL SIDEBAR ==========
        header_sidebar = QFrame()
        header_sidebar.setStyleSheet("background-color: #2c3e50;")
        header_sidebar.setFixedHeight(70)
        
        layout_header = QVBoxLayout()
        layout_header.setContentsMargins(20, 15, 20, 15)
        header_sidebar.setLayout(layout_header)
        
        label_nodo = QLabel("Nodo de Gestión")
        label_nodo.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        layout_header.addWidget(label_nodo)
        layout_sidebar.addWidget(header_sidebar)
        
        # ========== BOTONES DE MÓDULOS ==========
        modulos = [
            ('🏪', 'Tienda', self.abrir_tiendas),
            ('👥', 'Cliente', self.abrir_clientes),
            ('📦', 'Producto', self.abrir_productos),
            ('👨‍💼', 'Empleado', self.abrir_empleados),
            ('🛒', 'Venta', self.abrir_ventas),
            ('📋', 'Detalle Venta', self.abrir_detalle_venta),
            ('📊', 'Inventario', self.abrir_inventario),
        ]
        
        for icono, nombre, funcion in modulos:
            btn = self.crear_boton_modulo(icono, nombre, funcion)
            layout_sidebar.addWidget(btn)
        
        # Espacio flexible
        layout_sidebar.addStretch()
        
        # Añadir sidebar al layout principal
        layout_padre.addWidget(sidebar)
        
    def crear_boton_modulo(self, icono, nombre, funcion):
        """
        Crea un botón para un módulo del sidebar.
        """
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
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(funcion)
        return btn
        
    def crear_area_contenido(self, layout_padre):
        """
        Crea el área de contenido principal (barra superior + contenido).
        """
        # Frame del contenido
        frame_contenido = QFrame()
        frame_contenido.setStyleSheet("background-color: #ecf0f1;")
        
        # Layout del contenido
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(0, 0, 0, 0)
        layout_contenido.setSpacing(0)
        frame_contenido.setLayout(layout_contenido)
        
        # Crear barra superior
        self.crear_barra_superior(layout_contenido)
        
        # Crear área de bienvenida
        self.crear_area_bienvenida(layout_contenido)
        
        # Añadir al layout principal
        layout_padre.addWidget(frame_contenido)
        
    def crear_barra_superior(self, layout_padre):
        """
        Crea la barra superior con información del usuario.
        """
        barra = QFrame()
        barra.setFixedHeight(70)
        barra.setStyleSheet("background-color: white; border-bottom: 1px solid #dcdde1;")
        
        layout_barra = QHBoxLayout()
        layout_barra.setContentsMargins(30, 15, 30, 15)
        barra.setLayout(layout_barra)
        
        # Información del nodo
        label_nodo = QLabel("Nodo: Quito")
        label_nodo.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        layout_barra.addWidget(label_nodo)
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
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        btn_cerrar.setCursor(Qt.PointingHandCursor)
        btn_cerrar.clicked.connect(self.cerrar_sesion)
        
        layout_barra.addWidget(label_usuario)
        layout_barra.addWidget(btn_cerrar)
        
        layout_padre.addWidget(barra)
        
    def crear_area_bienvenida(self, layout_padre):
        """
        Crea el área de bienvenida con las tarjetas de módulos.
        """
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        # Widget contenedor
        widget_scroll = QWidget()
        layout_scroll = QVBoxLayout()
        layout_scroll.setContentsMargins(40, 30, 40, 30)
        layout_scroll.setSpacing(20)
        widget_scroll.setLayout(layout_scroll)
        
        # ========== TÍTULO DE BIENVENIDA ==========
        label_titulo = QLabel("Nodo de Gestión")
        label_titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        
        label_subtitulo = QLabel(f"Bienvenido, {self.datos_usuario['usuario']}.")
        label_subtitulo.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        
        label_descripcion = QLabel("Desde aquí puedes gestionar toda la información del sistema distribuido.")
        label_descripcion.setStyleSheet("font-size: 13px; color: #95a5a6; margin-bottom: 20px;")
        
        layout_scroll.addWidget(label_titulo)
        layout_scroll.addWidget(label_subtitulo)
        layout_scroll.addWidget(label_descripcion)
        
        # ========== GRID DE TARJETAS ==========
        self.crear_grid_tarjetas(layout_scroll)
        
        # Footer
        label_footer = QLabel("© 2026 - Sistema Corporativo")
        label_footer.setAlignment(Qt.AlignCenter)
        label_footer.setStyleSheet("font-size: 11px; color: #95a5a6; margin-top: 30px;")
        
        layout_scroll.addStretch()
        layout_scroll.addWidget(label_footer)
        
        scroll.setWidget(widget_scroll)
        layout_padre.addWidget(scroll)
        
    def crear_grid_tarjetas(self, layout_padre):
        """
        Crea el grid de tarjetas de módulos.
        """
        # Frame contenedor del grid
        frame_grid = QFrame()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        frame_grid.setLayout(grid_layout)
        
        # Definir tarjetas
        tarjetas = [
            ('🏪', 'Administrar Tiendas', 'Gestionar tiendas y\nsus ubicaciones.', self.abrir_tiendas),
            ('👥', 'Gestionar Clientes', 'Administrar la información\nde los clientes.', self.abrir_clientes),
            ('📦', 'Gestionar Productos', 'Administrar y modificar\nproductos.', self.abrir_productos),
            ('🛒', 'Gestionar Ventas', 'Consultar y gestionar\nlas ventas y detalles.', self.abrir_ventas),
            ('👨‍💼', 'Gestionar Empleados', 'Consultar y gestionar las\nventas y detalles.', self.abrir_empleados),
            ('📊', 'Gestionar Inventario', 'Controlar el inventario\nde las tiendas.', self.abrir_inventario),
        ]
        
        # Crear tarjetas en grid (3 columnas)
        row = 0
        col = 0
        for icono, titulo, descripcion, funcion in tarjetas:
            tarjeta = self.crear_tarjeta(icono, titulo, descripcion, funcion)
            grid_layout.addWidget(tarjeta, row, col)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        layout_padre.addWidget(frame_grid)
        
    def crear_tarjeta(self, icono, titulo, descripcion, funcion):
        """
        Crea una tarjeta de módulo.
        """
        tarjeta = QFrame()
        tarjeta.setFixedSize(280, 180)
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
        
        # Layout de la tarjeta
        layout_tarjeta = QVBoxLayout()
        layout_tarjeta.setContentsMargins(20, 20, 20, 20)
        layout_tarjeta.setAlignment(Qt.AlignCenter)
        tarjeta.setLayout(layout_tarjeta)
        
        # Icono
        label_icono = QLabel(icono)
        label_icono.setStyleSheet("font-size: 48px;")
        label_icono.setAlignment(Qt.AlignCenter)
        
        # Título
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("font-size: 15px; font-weight: bold; color: #2c3e50;")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setWordWrap(True)
        
        # Descripción
        label_desc = QLabel(descripcion)
        label_desc.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        label_desc.setAlignment(Qt.AlignCenter)
        label_desc.setWordWrap(True)
        
        layout_tarjeta.addWidget(label_icono)
        layout_tarjeta.addSpacing(10)
        layout_tarjeta.addWidget(label_titulo)
        layout_tarjeta.addSpacing(5)
        layout_tarjeta.addWidget(label_desc)
        
        # Evento de clic
        tarjeta.mousePressEvent = lambda event: funcion()
        
        return tarjeta
        
    # ============================================================
    # FUNCIONES DE NAVEGACIÓN A MÓDULOS
    # ============================================================
    
    def abrir_tiendas(self):
        """Abre el módulo de Tiendas"""
        print("TODO: Abrir vista de Tiendas")
        # TODO: Implementar vista de tiendas
        
    def abrir_clientes(self):
        """Abre el módulo de Clientes"""
        if self.ventana_activa:
            self.ventana_activa.close()
        self.ventana_activa = ClienteView(self.datos_usuario)
        self.ventana_activa.show()
        
    def abrir_productos(self):
        """Abre el módulo de Productos"""
        if self.ventana_activa:
            self.ventana_activa.close()
        self.ventana_activa = ProductoView(self.datos_usuario)
        self.ventana_activa.show()
        
    def abrir_empleados(self):
        """Abre el módulo de Empleados"""
        print("TODO: Abrir vista de Empleados")
        # TODO: Implementar vista de empleados
        
    def abrir_ventas(self):
        """Abre el módulo de Ventas"""
        print("TODO: Abrir vista de Ventas")
        # TODO: Implementar vista de ventas
        
    def abrir_detalle_venta(self):
        """Abre el módulo de Detalle Venta"""
        print("TODO: Abrir vista de Detalle Venta")
        # TODO: Implementar vista de detalle venta
        
    def abrir_inventario(self):
        """Abre el módulo de Inventario"""
        print("TODO: Abrir vista de Inventario")
        # TODO: Implementar vista de inventario
        
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        from views.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()