"""
config/credenciales.py
======================
Gestión de credenciales temporales del sistema.

⚠️ TODO: Reemplazar por validación con SQL Server
Estas credenciales están "quemadas" temporalmente.
Cuando se implemente SQL Server, se debe eliminar este archivo
y validar contra la tabla 'usuario' en la base de datos.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

# ============================================================
# CREDENCIALES TEMPORALES (HARDCODED)
# ============================================================
# TODO: Reemplazar por validación con SQL Server
# Formato: usuario: (contraseña, nodo, nombre_completo)

USUARIOS_TEMPORALES = {
    # Usuario del Nodo de Gestión (Quito)
    'admin': {
        'password': '1234',
        'nodo': 'gestion',
        'ciudad': 'Quito',
        'nombre_completo': 'Administrador del Sistema'
    },
    
    # Usuario del Nodo de Operación (Loja)
    'operador': {
        'password': '1234',
        'nodo': 'operacion',
        'ciudad': 'Loja',
        'nombre_completo': 'Operador de Sede'
    }
}


def validar_credenciales(usuario, password):
    """
    Valida las credenciales del usuario de forma temporal.
    
    ⚠️ TODO: Reemplazar por consulta SQL Server:
    
    SELECT u.usuario, u.nodo, u.nombre_completo, t.ciudad
    FROM usuario u
    INNER JOIN tienda t ON u.idTienda = t.idTienda
    WHERE u.usuario = ? AND u.password = HASHBYTES('SHA2_256', ?)
    AND u.activo = 1
    
    Args:
        usuario (str): Nombre de usuario
        password (str): Contraseña en texto plano
        
    Returns:
        dict: Datos del usuario si es válido, None si no
        {
            'usuario': 'admin',
            'nodo': 'gestion',
            'ciudad': 'Quito',
            'nombre_completo': 'Administrador del Sistema'
        }
    """
    # TODO: Reemplazar por conexión SQL Server
    
    # Validación temporal con diccionario
    if usuario in USUARIOS_TEMPORALES:
        datos_usuario = USUARIOS_TEMPORALES[usuario]
        if datos_usuario['password'] == password:
            return {
                'usuario': usuario,
                'nodo': datos_usuario['nodo'],
                'ciudad': datos_usuario['ciudad'],
                'nombre_completo': datos_usuario['nombre_completo']
            }
    
    return None


def obtener_nodo_usuario(usuario):
    """
    Obtiene el nodo al que pertenece un usuario.
    
    ⚠️ TODO: Reemplazar por consulta SQL Server
    
    Args:
        usuario (str): Nombre de usuario
        
    Returns:
        str: 'gestion' o 'operacion', None si no existe
    """
    # TODO: Reemplazar por SQL Server
    if usuario in USUARIOS_TEMPORALES:
        return USUARIOS_TEMPORALES[usuario]['nodo']
    return None