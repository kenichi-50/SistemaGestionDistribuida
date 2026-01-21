"""
views/login_view.py
===================
Ventana de inicio de sesión del sistema.
Diseño basado en la interfaz proporcionada.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from config.credenciales import validar_credenciales
from views.dashboard_gestion import DashboardGestion
from views.dashboard_loja import DashboardOperacion


class LoginView(QWidget):
    """
    Ventana de inicio de sesión.
    
    Credenciales temporales:
    - admin / 1234 → Nodo de Gestión (Quito)
    - operador / 1234 → Nodo de Operación (Loja)
    """
    
    def __init__(self):
        super().__init__()
        self.dashboard = None
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """
        Configura la interfaz de usuario del login.
        """
        # Configuración de la ventana
        self.setWindowTitle("Sistema de Gestión Distribuida")
        self.showMaximized()
        self.setStyleSheet("background-color: #e8e8e8;")
        
        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)
        self.setLayout(layout_principal)
        
        # Crear formulario de login
        self.crear_formulario_login(layout_principal)
        
    def crear_formulario_login(self, layout_padre):
        """
        Crea el formulario de login centrado.
        """
        # Frame contenedor (tarjeta blanca)
        frame_login = QFrame()
        frame_login.setFixedSize(450, 450)
        frame_login.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Layout del formulario
        layout_form = QVBoxLayout()
        layout_form.setContentsMargins(50, 50, 50, 50)
        layout_form.setSpacing(20)
        frame_login.setLayout(layout_form)
        
        # ========== TÍTULO ==========
        label_titulo = QLabel("SISTEMA DE GESTIÓN\nDISTRIBUIDA")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            line-height: 1.4;
        """)
        
        label_subtitulo = QLabel("Acceso al sistema")
        label_subtitulo.setAlignment(Qt.AlignCenter)
        label_subtitulo.setStyleSheet("""
            font-size: 13px;
            color: #7f8c8d;
            margin-bottom: 20px;
        """)
        
        # ========== CAMPO USUARIO ==========
        label_usuario = QLabel("Usuario")
        label_usuario.setStyleSheet("""
            font-size: 13px;
            color: #2c3e50;
            font-weight: 500;
        """)
        
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su usuario")
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 12px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        self.input_usuario.setMinimumHeight(40)
        
        # ========== CAMPO CONTRASEÑA ==========
        label_password = QLabel("Contraseña")
        label_password.setStyleSheet("""
            font-size: 13px;
            color: #2c3e50;
            font-weight: 500;
        """)
        
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("""
            QLineEdit {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 12px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        self.input_password.setMinimumHeight(40)
        
        # Enter para login
        self.input_password.returnPressed.connect(self.iniciar_sesion)
        
        # ========== BOTÓN INICIAR SESIÓN ==========
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 14px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
            QPushButton:pressed {
                background-color: #1a252f;
            }
        """)
        self.btn_login.setMinimumHeight(45)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self.iniciar_sesion)
        
        # ========== BOTÓN SALIR ==========
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setStyleSheet("""
            QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dfe6e9;
            }
            QPushButton:pressed {
                background-color: #dcdde1;
            }
        """)
        self.btn_salir.setMinimumHeight(40)
        self.btn_salir.setCursor(Qt.PointingHandCursor)
        self.btn_salir.clicked.connect(self.close)

        # ========== FOOTER ==========
        label_footer = QLabel("© 2026 - Sistema Corporativo")
        label_footer.setAlignment(Qt.AlignCenter)
        label_footer.setStyleSheet("""
            font-size: 11px;
            color: #95a5a6;
            margin-top: 20px;
        """)
        
        # ========== AGREGAR AL LAYOUT ==========
        layout_form.addWidget(label_titulo)
        layout_form.addWidget(label_subtitulo)
        layout_form.addSpacing(10)
        layout_form.addWidget(label_usuario)
        layout_form.addWidget(self.input_usuario)
        layout_form.addWidget(label_password)
        layout_form.addWidget(self.input_password)
        layout_form.addSpacing(10)
        layout_form.addWidget(self.btn_login)
        layout_form.addWidget(self.btn_salir)
        layout_form.addStretch()
        layout_form.addWidget(label_footer)
        
        # Añadir formulario al layout principal
        layout_padre.addWidget(frame_login, alignment=Qt.AlignCenter)
        
    def iniciar_sesion(self):
        """
        Procesa el inicio de sesión.
        
        Valida las credenciales y redirige al dashboard correspondiente
        según el nodo del usuario.
        
        ⚠️ TODO: Reemplazar validar_credenciales() por consulta SQL Server
        """
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()
        
        # Validar campos vacíos
        if not usuario or not password:
            self.mostrar_error("Por favor complete todos los campos")
            return
        
        # ⚠️ TODO: Reemplazar por validación con SQL Server
        # Validar credenciales
        datos_usuario = validar_credenciales(usuario, password)
        
        if datos_usuario:
            # Login exitoso
            self.abrir_dashboard(datos_usuario)
        else:
            # Login fallido
            self.mostrar_error("Usuario o contraseña incorrectos")
            self.input_password.clear()
            self.input_usuario.setFocus()
            
    def abrir_dashboard(self, datos_usuario):
        """
        Abre el dashboard correspondiente según el nodo del usuario.
        
        Args:
            datos_usuario (dict): Información del usuario autenticado
        """
        nodo = datos_usuario['nodo']
        
        # Cerrar ventana de login
        self.close()
        
        # Abrir dashboard según el nodo
        if nodo == 'gestion':
            self.dashboard = DashboardGestion(datos_usuario)
        elif nodo == 'operacion':
            self.dashboard = DashboardOperacion(datos_usuario)
        else:
            self.mostrar_error("Nodo no reconocido")
            return
            
        self.dashboard.show()
        
    def mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error.
        
        Args:
            mensaje (str): Mensaje a mostrar
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error de Autenticación")
        msg.setText(mensaje)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #2c3e50;
                font-size: 13px;
            }
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        msg.exec_()