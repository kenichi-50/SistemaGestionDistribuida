"""
views/dashboard_loja.py
=======================
Dashboard del Nodo de Operación (Loja).

Módulos disponibles:
- Cliente (CRUD completo)
- Producto (SOLO LECTURA)
- Empleado (solo empleados de Loja)
- Venta (solo ventas de Loja)
- Detalle Venta (consulta)
- Inventario (solo inventario de Loja)

IMPORTANTE: NO tiene acceso al módulo Tienda

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DashboardLoja(QMainWindow):
    """
    Dashboard principal del Nodo de Operación (Loja).
    """
    
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.modulo_actual = None
        self.init_ui()
        
    def init_ui(self):
        """
        Inicializa la interfaz de usuario.
        """
        # Configuración de la ventana
        self.setWindowTitle("Sistema de Gestión Distribuida")
        self.setMinimumSize(1200, 700)
        self.showMaximized()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal (horizontal: sidebar + contenido)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # ==================== SIDEBAR ====================
        self.create_sidebar(main_layout)
        
        # ==================== CONTENIDO PRINCIPAL ====================
        self.create_main_content(main_layout)
        
    def create_sidebar(self, parent_layout):
        """
        Crea el sidebar lateral con los módulos.
        NOTA: NO incluye Tienda (solo disponible en Gestión)
        
        Args:
            parent_layout: Layout padre donde se añadirá el sidebar
        """
        # Frame del sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: #3d4d66;
                border: none;
            }
        """)
        
        # Layout del sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        sidebar.setLayout(sidebar_layout)
        
        # Título del sidebar
        sidebar_title = QLabel("Nodo de Operación")
        sidebar_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        sidebar_title.setStyleSheet("""
            color: white;
            padding: 25px 20px;
            background-color: #2c3a4f;
        """)
        sidebar_layout.addWidget(sidebar_title)
        
        # Módulos disponibles (SIN Tienda)
        modulos = [
            {"nombre": "Cliente", "icono": "👤"},
            {"nombre": "Producto", "icono": "📦"},
            {"nombre": "Empleado", "icono": "👷"},
            {"nombre": "Venta", "icono": "🛒"},
            {"nombre": "Detalle Venta", "icono": "📄"},
            {"nombre": "Inventario", "icono": "📊"}
        ]
        
        # Crear botones para cada módulo
        self.sidebar_buttons = {}
        for modulo in modulos:
            btn = self.create_sidebar_button(modulo["icono"], modulo["nombre"])
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[modulo["nombre"]] = btn
        
        # Stretch al final
        sidebar_layout.addStretch()
        
        parent_layout.addWidget(sidebar)
        
    def create_sidebar_button(self, icono, texto):
        """
        Crea un botón para el sidebar.
        
        Args:
            icono (str): Emoji del icono
            texto (str): Texto del botón
            
        Returns:
            QPushButton: Botón configurado
        """
        btn = QPushButton(f"  {icono}  {texto}")
        btn.setObjectName("sidebar_button")
        btn.setCheckable(True)
        btn.setFont(QFont("Segoe UI", 11))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton#sidebar_button {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding: 18px 20px;
                font-size: 14px;
            }
            QPushButton#sidebar_button:hover {
                background-color: #4a5d7c;
            }
            QPushButton#sidebar_button:checked {
                background-color: #4a5d7c;
                border-left: 4px solid #4299e1;
            }
        """)
        
        # Conectar evento
        btn.clicked.connect(lambda: self.on_modulo_clicked(texto))
        
        return btn
        
    def create_main_content(self, parent_layout):
        """
        Crea el área de contenido principal.
        
        Args:
            parent_layout: Layout padre
        """
        # Widget contenedor
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #f5f7fa;")
        
        # Layout del contenido
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_widget.setLayout(content_layout)
        
        # ==================== HEADER ====================
        self.create_header(content_layout)
        
        # ==================== ÁREA DE CONTENIDO ====================
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f7fa;
            }
        """)
        
        # Widget del scroll
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(30, 30, 30, 30)
        self.scroll_layout.setSpacing(20)
        self.scroll_content.setLayout(self.scroll_layout)
        
        scroll.setWidget(self.scroll_content)
        content_layout.addWidget(scroll)
        
        # Mostrar página de bienvenida por defecto
        self.show_welcome_page()
        
        parent_layout.addWidget(content_widget)
        
    def create_header(self, parent_layout):
        """
        Crea el header superior.
        
        Args:
            parent_layout: Layout padre
        """
        # Frame del header
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame#header {
                background-color: white;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        
        # Layout del header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(30, 0, 30, 0)
        header.setLayout(header_layout)
        
        # Info del nodo
        nodo_label = QLabel(f"Nodo: {self.datos_usuario['ciudad']}")
        nodo_label.setFont(QFont("Segoe UI", 11))
        nodo_label.setStyleSheet("color: #718096;")
        
        header_layout.addWidget(nodo_label)
        header_layout.addStretch()
        
        # Icono usuario
        user_icon = QLabel("👤")
        user_icon.setFont(QFont("Segoe UI", 16))
        user_icon.setStyleSheet("color: #4a5568;")
        
        # Nombre usuario
        user_label = QLabel(self.datos_usuario['usuario'])
        user_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        user_label.setStyleSheet("color: #2d3748; margin-left: 5px;")
        
        # Botón cerrar sesión
        logout_btn = QPushButton("Cerrar Sesión")
        logout_btn.setObjectName("cerrar_sesion")
        logout_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setFixedHeight(35)
        logout_btn.setStyleSheet("""
            QPushButton#cerrar_sesion {
                background-color: #3d5a80;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 0 20px;
            }
            QPushButton#cerrar_sesion:hover {
                background-color: #2e4660;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        
        header_layout.addWidget(user_icon)
        header_layout.addWidget(user_label)
        header_layout.addSpacing(20)
        header_layout.addWidget(logout_btn)
        
        parent_layout.addWidget(header)
        
    def show_welcome_page(self):
        """
        Muestra la página de bienvenida con las tarjetas de módulos.
        """
        # Limpiar contenido actual
        self.clear_content()
        
        # Título de bienvenida
        welcome_title = QLabel("Nodo de Operación")
        welcome_title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        welcome_title.setStyleSheet("color: #2d3748;")
        
        # Mensaje de bienvenida
        welcome_msg = QLabel(f"Bienvenido, {self.datos_usuario['nombre_completo']}.")
        welcome_msg.setFont(QFont("Segoe UI", 14))
        welcome_msg.setStyleSheet("color: #4a5568; margin-top: 5px;")
        
        # Descripción
        description = QLabel("Desde aquí puedes consultar y gestionar cierta información del sistema distribuido.")
        description.setFont(QFont("Segoe UI", 12))
        description.setStyleSheet("color: #718096; margin-top: 10px; margin-bottom: 30px;")
        
        self.scroll_layout.addWidget(welcome_title)
        self.scroll_layout.addWidget(welcome_msg)
        self.scroll_layout.addWidget(description)
        
        # Grid de tarjetas
        self.create_module_cards()
        
        self.scroll_layout.addStretch()
        
    def create_module_cards(self):
        """
        Crea las tarjetas de los módulos.
        """
        # Grid layout
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Definición de módulos (SIN Tienda)
        modules = [
            {
                "nombre": "Cliente",
                "icono": "👥",
                "titulo": "Gestionar Clientes",
                "descripcion": "Gestionar tiendas y\nsus ubicaciones.",
                "enabled": True
            },
            {
                "nombre": "Producto",
                "icono": "📦",
                "titulo": "Ver Productos",
                "descripcion": "Ver y administrar información\nproducto.",
                "enabled": True  # Solo lectura
            },
            {
                "nombre": "Empleado",
                "icono": "👷",
                "titulo": "Gestionar Empleados",
                "descripcion": "Gestionar trestionar\nde Laoperaciones.",
                "enabled": True
            },
            {
                "nombre": "Venta",
                "icono": "🛒",
                "titulo": "Gestionar Ventas",
                "descripcion": "Consultar y gestionar\nlas ventas y detalles.",
                "enabled": True
            },
            {
                "nombre": "Detalle Venta",
                "icono": "📄",
                "titulo": "Ver Detalles de Venta",
                "descripcion": "Consultar detalles\nde ventas realizadas.",
                "enabled": True
            },
            {
                "nombre": "Inventario",
                "icono": "📊",
                "titulo": "Inventario",
                "descripcion": "Consultar inventario\nlocal.",
                "enabled": True
            }
        ]
        
        # Crear tarjetas
        row, col = 0, 0
        for module in modules:
            card = self.create_card(
                module["icono"],
                module["titulo"],
                module["descripcion"],
                module["nombre"],
                module.get("enabled", True)
            )
            grid.addWidget(card, row, col)
            
            col += 1
            if col > 2:  # 3 columnas
                col = 0
                row += 1
        
        self.scroll_layout.addLayout(grid)
        
    def create_card(self, icono, titulo, descripcion, modulo, enabled=True):
        """
        Crea una tarjeta de módulo.
        
        Args:
            icono (str): Emoji del icono
            titulo (str): Título de la tarjeta
            descripcion (str): Descripción
            modulo (str): Nombre del módulo
            enabled (bool): Si está habilitado para edición
            
        Returns:
            QFrame: Tarjeta configurada
        """
        # Frame de la tarjeta
        card = QFrame()
        card.setFixedSize(280, 180)
        
        if enabled:
            card.setCursor(Qt.PointingHandCursor)
            card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                }
                QFrame:hover {
                    border: 1px solid #cbd5e0;
                    background-color: #f7fafc;
                }
            """)
        else:
            # Estilo para módulos de solo lectura
            card.setStyleSheet("""
                QFrame {
                    background-color: #f7fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    opacity: 0.7;
                }
            """)
        
        # Layout de la tarjeta
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(6)
        card.setLayout(card_layout)
        
        # Icono
        icon_label = QLabel(icono)
        icon_label.setFont(QFont("Segoe UI", 36))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            background-color: {'#edf2f7' if enabled else '#e2e8f0'};
            border-radius: 30px;
            padding: 15px;
        """)
        icon_label.setFixedSize(70, 70)
        
        # Título
        title_label = QLabel(titulo)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title_label.setStyleSheet(f"color: {'#2d3748' if enabled else '#a0aec0'};")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Descripción
        desc_label = QLabel(descripcion)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setStyleSheet(f"color: {'#718096' if enabled else '#a0aec0'};")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        # Añadir elementos
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)
        card_layout.addStretch()
        
        # Conectar evento de clic solo si está habilitado
        if enabled:
            card.mousePressEvent = lambda event: self.on_modulo_clicked(modulo)
        
        return card
        
    def on_modulo_clicked(self, modulo):
        """
        Maneja el clic en un módulo.
        
        Args:
            modulo (str): Nombre del módulo
        """
        print(f"Módulo seleccionado: {modulo}")
        
        # Actualizar botones del sidebar
        for nombre, btn in self.sidebar_buttons.items():
            btn.setChecked(nombre == modulo)
        
        # Abrir vista del módulo
        if modulo == "Cliente":
            self.open_cliente_view()
        elif modulo == "Producto":
            self.open_producto_view()
        elif modulo == "Empleado":
            self.open_empleado_view()
        elif modulo == "Venta":
            self.open_venta_view()
        elif modulo == "Detalle Venta":
            self.open_detalle_venta_view()
        elif modulo == "Inventario":
            self.open_inventario_view()
        
    def open_cliente_view(self):
        """
        Abre la vista de Clientes.
        """
        from views.tablas.cliente_view import ClienteView
        self.ventana_clientes = ClienteView(self.datos_usuario)
        self.ventana_clientes.show()


    def open_producto_view(self):
        """
        Abre la vista de Productos (SOLO LECTURA).
        """
        from views.tablas.producto_view import ProductoView
        self.ventana_productos = ProductoView(self.datos_usuario)
        self.ventana_productos.show()


    def open_empleado_view(self):
        """
        Abre la vista de Empleados.
        """
        from views.tablas.empleado_view import EmpleadoView
        self.ventana_empleados = EmpleadoView(self.datos_usuario)
        self.ventana_empleados.show()


    def open_venta_view(self):
        """
        Abre la vista de Ventas.
        """
        from views.tablas.venta_view import VentaView
        self.ventana_ventas = VentaView(self.datos_usuario)
        self.ventana_ventas.show()


    def open_detalle_venta_view(self):
        """
        Abre la vista de Detalle de Venta.
        """
        from views.tablas.detalle_venta_view import DetalleVentaView
        self.ventana_detalle_ventas = DetalleVentaView(self.datos_usuario)
        self.ventana_detalle_ventas.show()


    def open_inventario_view(self):
        """
        Abre la vista de Inventario.
        """
        from views.tablas.inventario_view import InventarioView
        self.ventana_inventario = InventarioView(self.datos_usuario)
        self.ventana_inventario.show()

    def show_module_view(self, view_widget):
        """
        Muestra una vista de módulo en el contenido principal.
        
        Args:
            view_widget: Widget de la vista a mostrar
        """
        self.clear_content()
        self.scroll_layout.addWidget(view_widget)
        self.scroll_layout.addStretch()
        
    def clear_content(self):
        """
        Limpia el contenido actual del scroll area.
        """
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
    def logout(self):
        """
        Cierra sesión y vuelve al login.
        """
        from views.login_view import LoginWindow
        
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()