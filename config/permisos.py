"""
config/permisos.py
==================
Configuración de permisos y reglas de acceso por nodo.

Define qué módulos y operaciones puede realizar cada nodo del sistema.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

# ============================================================
# PERMISOS POR NODO
# ============================================================

PERMISOS = {
    # Nodo de Gestión (Quito)
    'gestion': {
        'tienda': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'descripcion': 'CRUD completo de tiendas'
        },
        'cliente': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'descripcion': 'CRUD completo de clientes'
        },
        'producto': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'descripcion': 'CRUD completo de productos'
        },
        'empleado': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'filtro': 'ciudad = "Quito"',  # Solo empleados de Quito
            'descripcion': 'Solo empleados de Quito'
        },
        'venta': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'filtro': 'idTienda IN (SELECT idTienda FROM tienda WHERE ciudad = "Quito")',
            'descripcion': 'Solo ventas de Quito'
        },
        'detalle_venta': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'descripcion': 'Detalles de ventas de Quito'
        },
        'inventario': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'filtro': 'fkIdTienda IN (SELECT idTienda FROM tienda WHERE ciudad = "Quito")',
            'descripcion': 'Solo inventario de Quito'
        }
    },
    
    # Nodo de Operación (Loja)
    'operacion': {
        'tienda': {
            'ver': False,  # ⚠️ NO puede ver tiendas
            'crear': False,
            'editar': False,
            'eliminar': False,
            'descripcion': 'Sin acceso a módulo Tienda'
        },
        'cliente': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'descripcion': 'CRUD completo de clientes'
        },
        'producto': {
            'ver': True,       # Solo lectura
            'crear': False,
            'editar': False,
            'eliminar': False,
            'descripcion': 'Solo lectura de productos'
        },
        'empleado': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'filtro': 'ciudad = "Loja"',  # Solo empleados de Loja
            'descripcion': 'Solo empleados de Loja'
        },
        'venta': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'filtro': 'idTienda IN (SELECT idTienda FROM tienda WHERE ciudad = "Loja")',
            'descripcion': 'Solo ventas de Loja'
        },
        'detalle_venta': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'descripcion': 'Detalles de ventas de Loja'
        },
        'inventario': {
            'ver': True,
            'crear': True,
            'editar': True,
            'eliminar': True,
            'filtro': 'fkIdTienda IN (SELECT idTienda FROM tienda WHERE ciudad = "Loja")',
            'descripcion': 'Solo inventario de Loja'
        }
    }
}


# ============================================================
# MÓDULOS DISPONIBLES POR NODO
# ============================================================

MODULOS_POR_NODO = {
    'gestion': [
        'tienda',
        'cliente',
        'producto',
        'empleado',
        'venta',
        'detalle_venta',
        'inventario'
    ],
    'operacion': [
        # 'tienda',  # ⚠️ NO incluido
        'cliente',
        'producto',
        'empleado',
        'venta',
        'detalle_venta',
        'inventario'
    ]
}


# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def tiene_permiso(nodo, modulo, accion):
    """
    Verifica si un nodo tiene permiso para realizar una acción en un módulo.
    
    Args:
        nodo (str): 'gestion' o 'operacion'
        modulo (str): Nombre del módulo (ej: 'cliente', 'producto')
        accion (str): 'ver', 'crear', 'editar', 'eliminar'
        
    Returns:
        bool: True si tiene permiso, False si no
    """
    if nodo not in PERMISOS:
        return False
    
    if modulo not in PERMISOS[nodo]:
        return False
    
    return PERMISOS[nodo][modulo].get(accion, False)


def obtener_filtro_sql(nodo, modulo):
    """
    Obtiene el filtro SQL que debe aplicarse para un módulo en un nodo.
    
    Args:
        nodo (str): 'gestion' o 'operacion'
        modulo (str): Nombre del módulo
        
    Returns:
        str: Filtro SQL o None si no aplica
    """
    if nodo not in PERMISOS:
        return None
    
    if modulo not in PERMISOS[nodo]:
        return None
    
    return PERMISOS[nodo][modulo].get('filtro', None)


def modulo_visible(nodo, modulo):
    """
    Verifica si un módulo debe ser visible en el sidebar para un nodo.
    
    Args:
        nodo (str): 'gestion' o 'operacion'
        modulo (str): Nombre del módulo
        
    Returns:
        bool: True si debe mostrarse, False si no
    """
    if nodo not in MODULOS_POR_NODO:
        return False
    
    return modulo in MODULOS_POR_NODO[nodo]


def obtener_modulos_nodo(nodo):
    """
    Obtiene la lista de módulos disponibles para un nodo.
    
    Args:
        nodo (str): 'gestion' o 'operacion'
        
    Returns:
        list: Lista de nombres de módulos
    """
    return MODULOS_POR_NODO.get(nodo, [])