"""
main.py
=======
Punto de entrada principal del Sistema de Gestión Distribuida.
Inicia la aplicación mostrando la ventana de login.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from views.login_view import LoginView


def main():
    """
    Función principal que inicia la aplicación.
    """
    # Crear aplicación
    app = QApplication(sys.argv)
    
    # Configurar fuente global
    app.setFont(QFont("Segoe UI", 10))
    
    # Habilitar high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Crear y mostrar ventana de login
    login = LoginView()
    login.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()