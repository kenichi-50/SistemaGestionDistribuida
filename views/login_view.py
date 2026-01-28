"""
views/login_view.py
===================
Ventana de inicio de sesión del sistema.

Credenciales de prueba:
- admin / 1234 → Nodo de Gestión (Quito)
- operador / 1234 → Nodo de Operación (Loja)

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.conexion import validar_usuario_sql


class LoginWindow(QMainWindow):
    """
    Ventana de inicio de sesión.
    Valida credenciales y redirige al dashboard correspondiente.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Configuración de ventana
        self.setWindowTitle("Sistema de Gestión Distribuida")
        self.setFixedSize(500, 600)
        self.center_window()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        central_widget.setStyleSheet("""
            QWidget {
                background-color: #e8eef3;
            }
        """)

        # Contenedor formulario
        form_container = QFrame()
        form_container.setFixedSize(400, 500)
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #d0d7de;
            }
        """)

        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(20)

        # ---------- TÍTULOS ----------
        title = QLabel("SISTEMA DE GESTIÓN\nDISTRIBUIDA")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")

        subtitle = QLabel("Acceso al sistema")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #7f8c8d;")

        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addSpacing(30)

        # ---------- USUARIO ----------
        lbl_user = QLabel("Usuario")
        lbl_user.setFont(QFont("Segoe UI", 10, QFont.Bold))

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingrese su usuario")
        self.user_input.setFixedHeight(45)
        self.user_input.setFont(QFont("Segoe UI", 11))
        self.user_input.setStyleSheet(self.input_style())

        form_layout.addWidget(lbl_user)
        form_layout.addWidget(self.user_input)

        # ---------- CONTRASEÑA ----------
        lbl_pass = QLabel("Contraseña")
        lbl_pass.setFont(QFont("Segoe UI", 10, QFont.Bold))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setFont(QFont("Segoe UI", 11))
        self.password_input.setStyleSheet(self.input_style())
        self.password_input.returnPressed.connect(self.handle_login)

        form_layout.addWidget(lbl_pass)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(20)

        # ---------- BOTÓN ----------
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setFixedHeight(50)
        btn_login.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #3d5a80;
                color: white;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #2e4660;
            }
        """)
        btn_login.clicked.connect(self.handle_login)

        form_layout.addWidget(btn_login)
        form_layout.addStretch()

        # ---------- FOOTER ----------
        footer = QLabel("© 2026 - Sistema Corporativo")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QFont("Segoe UI", 9))
        footer.setStyleSheet("color: #95a5a6;")

        form_layout.addWidget(footer)

        # Centrado
        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(form_container)
        wrapper.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(wrapper)
        main_layout.addStretch()

    def input_style(self):
        return """
            QLineEdit {
                border: 1px solid #d0d7de;
                border-radius: 8px;
                padding: 0 15px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3d5a80;
            }
        """

    def center_window(self):
        screen = self.screen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

    def handle_login(self):
        usuario = self.user_input.text().strip()
        password = self.password_input.text().strip()

        if not usuario or not password:
            self.show_error("Por favor complete todos los campos")
            return

        resultado = validar_usuario_sql(usuario, password)

        if not resultado:
            self.show_error("Usuario o contraseña incorrectos")
            self.password_input.clear()
            return

        if resultado['nodo'] == 'gestion':
            from views.dashboard_gestion import DashboardGestion
            self.dashboard = DashboardGestion(resultado)
        else:
            from views.dashboard_loja import DashboardLoja
            self.dashboard = DashboardLoja(resultado)

        self.dashboard.show()
        self.close()

    def show_error(self, mensaje):
        QMessageBox.warning(self, "Error de Autenticación", mensaje)
