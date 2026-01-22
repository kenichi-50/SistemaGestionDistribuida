"""
database/conexion.py
====================
Conexiones a SQL Server para el sistema distribuido.

Nodos:
- Gestión (Quito): Base de datos NexusTech_Quito
- Operación (Loja): Base de datos NexusTech_Loja

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

import pyodbc


# ============================================================
# CONFIGURACIÓN DE CONEXIONES
# ============================================================

CONFIG_QUITO = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'HARRYPC',
    'database': 'NexusTech_Quito',
    'username': 'sa',
    'password': 'P@ssw0rd',
    'trust_certificate': 'yes'
}

CONFIG_LOJA = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'JOEL',
    'database': 'NexusTech_Loja',
    'username': 'sa',
    'password': 'P@ssw0rd',
    'trust_certificate': 'yes'
}


# ============================================================
# FUNCIONES DE CONEXIÓN
# ============================================================

def conectar_quito():
    """
    Establece conexión con el Nodo de Gestión (Quito).
    
    Returns:
        connection: Objeto de conexión pyodbc o None si falla
    """
    try:
        conexion = pyodbc.connect(
            f"DRIVER={{{CONFIG_QUITO['driver']}}};"
            f"SERVER={CONFIG_QUITO['server']};"
            f"DATABASE={CONFIG_QUITO['database']};"
            f"UID={CONFIG_QUITO['username']};"
            f"PWD={CONFIG_QUITO['password']};"
            f"TrustServerCertificate={CONFIG_QUITO['trust_certificate']};"
        )
        print("✓ Conectado al Nodo Quito (Gestión)")
        return conexion
    except pyodbc.Error as e:
        print(f"✗ Error al conectar con SQL Server (Nodo Quito): {e}")
        return None


def conectar_loja():
    """
    Establece conexión con el Nodo de Operación (Loja).
    
    Returns:
        connection: Objeto de conexión pyodbc o None si falla
    """
    try:
        conexion = pyodbc.connect(
            f"DRIVER={{{CONFIG_LOJA['driver']}}};"
            f"SERVER={CONFIG_LOJA['server']};"
            f"DATABASE={CONFIG_LOJA['database']};"
            f"UID={CONFIG_LOJA['username']};"
            f"PWD={CONFIG_LOJA['password']};"
            f"TrustServerCertificate={CONFIG_LOJA['trust_certificate']};"
        )
        print("✓ Conectado al Nodo Loja (Operación)")
        return conexion
    except pyodbc.Error as e:
        print(f"✗ Error al conectar con SQL Server (Nodo Loja): {e}")
        return None


def conectar_segun_nodo(nodo):
    """
    Conecta según el tipo de nodo.
    
    Args:
        nodo (str): 'gestion' o 'operacion'
        
    Returns:
        connection: Conexión correspondiente
    """
    if nodo == 'gestion':
        return conectar_quito()
    elif nodo == 'operacion':
        return conectar_loja()
    else:
        print(f"✗ Nodo '{nodo}' no reconocido")
        return None


def cerrar_conexion(conexion):
    """
    Cierra una conexión de forma segura.
    
    Args:
        conexion: Objeto de conexión a cerrar
    """
    if conexion:
        try:
            conexion.close()
            print("✓ Conexión cerrada correctamente")
        except Exception as e:
            print(f"✗ Error al cerrar conexión: {e}")


# ============================================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================================

def validar_usuario_sql(usuario, password):
    """
    Valida credenciales de usuario contra SQL Server.
    
    NOTA: Por ahora probamos con Nodo Loja.
    En producción, deberías tener una tabla 'usuario' centralizada.
    
    Args:
        usuario (str): Nombre de usuario
        password (str): Contraseña (en producción usar hash)
        
    Returns:
        dict: Datos del usuario si es válido, None si no
    """
    # Mapeo temporal de usuarios
    # En producción esto vendría de una tabla usuario
    usuarios_temporales = {
        'admin': {
            'password': '1234',
            'nodo': 'gestion',
            'ciudad': 'Quito',
            'nombre_completo': 'Administrador del Sistema'
        },
        'operador': {
            'password': '1234',
            'nodo': 'operacion',
            'ciudad': 'Loja',
            'nombre_completo': 'Operador de Sede'
        }
    }
    
    if usuario in usuarios_temporales:
        datos = usuarios_temporales[usuario]
        if datos['password'] == password:
            return {
                'usuario': usuario,
                'nodo': datos['nodo'],
                'ciudad': datos['ciudad'],
                'nombre_completo': datos['nombre_completo']
            }
    
    return None


# ============================================================
# FUNCIONES CRUD - CLIENTES (Nodo Loja)
# ============================================================

def obtener_clientes_loja():
    """
    Obtiene todos los clientes del Nodo Loja.
    
    Returns:
        list: Lista de diccionarios con datos de clientes
    """
    conexion = conectar_loja()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
            SELECT 
                idCliente,
                nombre,
                direccion,
                telefono,
                correo,
                fechaRegistro,
                rowguid
            FROM dbo.Cliente
            ORDER BY nombre
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        clientes = []
        for row in resultados:
            clientes.append({
                'id': row[0],
                'nombre': row[1],
                'direccion': row[2],
                'telefono': row[3],
                'correo': row[4],
                'fecha_registro': str(row[5]) if row[5] else '',
                'rowguid': str(row[6]) if row[6] else ''
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return clientes
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener clientes: {e}")
        cerrar_conexion(conexion)
        return []


def insertar_cliente_loja(nombre, direccion, telefono, correo):
    """
    Inserta un nuevo cliente en el Nodo Loja.
    
    Args:
        nombre (str): Nombre del cliente
        direccion (str): Dirección
        telefono (str): Teléfono
        correo (str): Correo electrónico
        
    Returns:
        bool: True si se insertó correctamente, False si no
    """
    conexion = conectar_loja()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO dbo.Cliente (nombre, direccion, telefono, correo)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, direccion, telefono, correo))
        conexion.commit()
        
        print(f"✓ Cliente '{nombre}' insertado correctamente")
        cursor.close()
        cerrar_conexion(conexion)
        return True
        
    except pyodbc.Error as e:
        print(f"✗ Error al insertar cliente: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def actualizar_cliente_loja(id_cliente, nombre, direccion, telefono, correo):
    """
    Actualiza un cliente existente en el Nodo Loja.
    
    Args:
        id_cliente (int): ID del cliente
        nombre (str): Nombre del cliente
        direccion (str): Dirección
        telefono (str): Teléfono
        correo (str): Correo electrónico
        
    Returns:
        bool: True si se actualizó correctamente, False si no
    """
    conexion = conectar_loja()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
            UPDATE dbo.Cliente
            SET nombre = ?, direccion = ?, telefono = ?, correo = ?
            WHERE idCliente = ?
        """
        cursor.execute(query, (nombre, direccion, telefono, correo, id_cliente))
        conexion.commit()
        
        print(f"✓ Cliente ID {id_cliente} actualizado correctamente")
        cursor.close()
        cerrar_conexion(conexion)
        return True
        
    except pyodbc.Error as e:
        print(f"✗ Error al actualizar cliente: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def eliminar_cliente_loja(id_cliente):
    """
    Elimina un cliente del Nodo Loja.
    
    Args:
        id_cliente (int): ID del cliente
        
    Returns:
        bool: True si se eliminó correctamente, False si no
    """
    conexion = conectar_loja()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM dbo.Cliente WHERE idCliente = ?"
        cursor.execute(query, (id_cliente,))
        conexion.commit()
        
        print(f"✓ Cliente ID {id_cliente} eliminado correctamente")
        cursor.close()
        cerrar_conexion(conexion)
        return True
        
    except pyodbc.Error as e:
        print(f"✗ Error al eliminar cliente: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


# ============================================================
# FUNCIONES CONSULTA - PRODUCTOS (SOLO LECTURA en Loja)
# ============================================================

def obtener_productos_loja():
    """
    Obtiene todos los productos (SOLO LECTURA).
    
    Los productos son gestionados desde Quito.
    Loja solo puede consultarlos.
    
    Returns:
        list: Lista de diccionarios con datos de productos
    """
    conexion = conectar_loja()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
            SELECT 
                p.id_producto,
                p.nombre,
                p.marca,
                p.modelo,
                p.categoria,
                p.precio_cents,
                p.stock_minimo
            FROM dbo.Producto_Info p
            ORDER BY p.nombre
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        productos = []
        for row in resultados:
            productos.append({
                'id': row[0],
                'nombre': row[1],
                'marca': row[2] if row[2] else '',
                'modelo': row[3] if row[3] else '',
                'categoria': row[4] if row[4] else '',
                'precio': row[5] / 100.0 if row[5] else 0.0,  # Convertir centavos a dólares
                'stock_minimo': row[6] if row[6] else 0
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return productos
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener productos: {e}")
        cerrar_conexion(conexion)
        return []


# ============================================================
# FUNCIONES CRUD - EMPLEADOS (Nodo Loja)
# ============================================================

def obtener_empleados_loja():
    """
    Obtiene todos los empleados del Nodo Loja.
    
    Returns:
        list: Lista de diccionarios con datos de empleados
    """
    conexion = conectar_loja()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
            SELECT 
                e.idEmpleado,
                e.nombre,
                e.telefono,
                e.cargo,
                e.fechaContratacion,
                e.fkIdTienda
            FROM dbo.Empleado_Loja e
            ORDER BY e.nombre
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        empleados = []
        for row in resultados:
            empleados.append({
                'id': row[0],
                'nombre': row[1],
                'telefono': row[2] if row[2] else '',
                'cargo': row[3] if row[3] else '',
                'fecha_contratacion': str(row[4]) if row[4] else '',
                'id_tienda': row[5]
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return empleados
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener empleados: {e}")
        cerrar_conexion(conexion)
        return []


def insertar_empleado_loja(nombre, telefono, cargo, id_tienda):
    """
    Inserta un nuevo empleado en el Nodo Loja.
    
    Args:
        nombre (str): Nombre del empleado
        telefono (str): Teléfono
        cargo (str): Cargo
        id_tienda (int): ID de la tienda (siempre 3 para Loja)
        
    Returns:
        bool: True si se insertó correctamente
    """
    conexion = conectar_loja()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO dbo.Empleado_Loja (nombre, telefono, cargo, fkIdTienda)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, telefono, cargo, id_tienda))
        conexion.commit()
        
        print(f"✓ Empleado '{nombre}' insertado correctamente")
        cursor.close()
        cerrar_conexion(conexion)
        return True
        
    except pyodbc.Error as e:
        print(f"✗ Error al insertar empleado: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def actualizar_empleado_loja(id_empleado, nombre, telefono, cargo):
    """
    Actualiza un empleado existente en el Nodo Loja.
    
    Args:
        id_empleado (int): ID del empleado
        nombre (str): Nombre
        telefono (str): Teléfono
        cargo (str): Cargo
        
    Returns:
        bool: True si se actualizó correctamente
    """
    conexion = conectar_loja()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
            UPDATE dbo.Empleado_Loja
            SET nombre = ?, telefono = ?, cargo = ?
            WHERE idEmpleado = ?
        """
        cursor.execute(query, (nombre, telefono, cargo, id_empleado))
        conexion.commit()
        
        print(f"✓ Empleado ID {id_empleado} actualizado correctamente")
        cursor.close()
        cerrar_conexion(conexion)
        return True
        
    except pyodbc.Error as e:
        print(f"✗ Error al actualizar empleado: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def eliminar_empleado_loja(id_empleado):
    """
    Elimina un empleado del Nodo Loja.
    
    Args:
        id_empleado (int): ID del empleado
        
    Returns:
        bool: True si se eliminó correctamente
    """
    conexion = conectar_loja()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM dbo.Empleado_Loja WHERE idEmpleado = ?"
        cursor.execute(query, (id_empleado,))
        conexion.commit()
        
        print(f"✓ Empleado ID {id_empleado} eliminado correctamente")
        cursor.close()
        cerrar_conexion(conexion)
        return True
        
    except pyodbc.Error as e:
        print(f"✗ Error al eliminar empleado: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


# ============================================================
# FUNCIONES CONSULTA - INVENTARIO (SOLO LECTURA en Loja)
# ============================================================

def obtener_inventario_loja():
    """
    Obtiene el inventario actual del Nodo Loja.
    
    El inventario NO se modifica manualmente.
    Se actualiza automáticamente con las ventas.
    
    Returns:
        list: Lista de diccionarios con el inventario
    """
    conexion = conectar_loja()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
            SELECT 
                i.fkIdTienda,
                i.fkIdProducto,
                i.stock,
                i.fechaActualizacion
            FROM dbo.Inventario_Loja i
            ORDER BY i.fkIdProducto
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        inventario = []
        for row in resultados:
            inventario.append({
                'id_tienda': row[0],
                'id_producto': row[1],
                'stock': row[2],
                'fecha_actualizacion': str(row[3]) if row[3] else ''
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return inventario
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener inventario: {e}")
        cerrar_conexion(conexion)
        return []


# ============================================================
# FUNCIONES CRUD - VENTAS (Nodo Loja)
# ============================================================

def obtener_ventas_loja():
    """
    Obtiene todas las ventas del Nodo Loja.
    
    Returns:
        list: Lista de diccionarios con datos de ventas
    """
    conexion = conectar_loja()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
            SELECT 
                v.idVenta,
                v.fechaVenta,
                v.totalCents,
                v.fkIdCliente,
                v.fkIdEmpleado,
                v.fkIdTienda,
                c.nombre as nombre_cliente
            FROM dbo.Venta_Loja v
            LEFT JOIN dbo.Cliente c ON v.fkIdCliente = c.idCliente
            ORDER BY v.fechaVenta DESC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        ventas = []
        for row in resultados:
            ventas.append({
                'id': row[0],
                'fecha': str(row[1]) if row[1] else '',
                'total': row[2] / 100.0 if row[2] else 0.0,  # Convertir centavos a dólares
                'id_cliente': row[3],
                'id_empleado': row[4],
                'id_tienda': row[5],
                'nombre_cliente': row[6] if row[6] else 'N/A'
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return ventas
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener ventas: {e}")
        cerrar_conexion(conexion)
        return []


def insertar_venta_loja(id_cliente, id_empleado, id_tienda, detalles):
    """
    Inserta una nueva venta con sus detalles en el Nodo Loja.
    
    Esta función realiza múltiples operaciones:
    1. Calcula el total de la venta
    2. Inserta la cabecera de venta
    3. Inserta los detalles de venta
    4. Actualiza el inventario
    
    Args:
        id_cliente (int): ID del cliente
        id_empleado (int): ID del empleado que realiza la venta
        id_tienda (int): ID de la tienda (siempre 3 para Loja)
        detalles (list): Lista de diccionarios con:
            {
                'id_producto': int,
                'cantidad': int,
                'precio_unitario': float
            }
    
    Returns:
        int: ID de la venta insertada, None si falla
    """
    conexion = conectar_loja()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor()
        
        # Calcular total en centavos
        total_cents = sum(int(d['precio_unitario'] * 100) * d['cantidad'] for d in detalles)
        
        # 1. Insertar cabecera de venta
        query_venta = """
            INSERT INTO dbo.Venta_Loja (totalCents, fkIdCliente, fkIdEmpleado, fkIdTienda)
            VALUES (?, ?, ?, ?);
            SELECT SCOPE_IDENTITY();
        """
        cursor.execute(query_venta, (total_cents, id_cliente, id_empleado, id_tienda))
        id_venta = cursor.fetchone()[0]
        
        # 2. Insertar detalles de venta
        query_detalle = """
            INSERT INTO dbo.DetalleVenta_Loja (fkIdVenta, nLineaId, fkIdProducto)
            VALUES (?, ?, ?)
        """
        for idx, detalle in enumerate(detalles, start=1):
            cursor.execute(query_detalle, (int(id_venta), idx, detalle['id_producto']))
        
        # 3. Actualizar inventario (restar stock)
        query_inventario = """
            UPDATE dbo.Inventario_Loja
            SET stock = stock - ?,
                fechaActualizacion = GETDATE()
            WHERE fkIdTienda = ? AND fkIdProducto = ?
        """
        for detalle in detalles:
            cursor.execute(query_inventario, (
                detalle['cantidad'],
                id_tienda,
                detalle['id_producto']
            ))
        
        conexion.commit()
        print(f"✓ Venta ID {id_venta} registrada correctamente con {len(detalles)} productos")
        
        cursor.close()
        cerrar_conexion(conexion)
        return int(id_venta)
        
    except pyodbc.Error as e:
        print(f"✗ Error al insertar venta: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return None


def obtener_detalle_venta_loja(id_venta):
    """
    Obtiene los detalles de una venta específica.
    
    Args:
        id_venta (int): ID de la venta
        
    Returns:
        list: Lista de diccionarios con los detalles
    """
    conexion = conectar_loja()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        query = """
            SELECT 
                dv.fkIdVenta,
                dv.nLineaId,
                dv.fkIdProducto,
                p.nombre as nombre_producto
            FROM dbo.DetalleVenta_Loja dv
            LEFT JOIN dbo.Producto_Info p ON dv.fkIdProducto = p.id_producto
            WHERE dv.fkIdVenta = ?
            ORDER BY dv.nLineaId
        """
        cursor.execute(query, (id_venta,))
        resultados = cursor.fetchall()
        
        detalles = []
        for row in resultados:
            detalles.append({
                'id_venta': row[0],
                'linea_id': row[1],
                'id_producto': row[2],
                'nombre_producto': row[3] if row[3] else 'N/A'
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return detalles
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener detalle de venta: {e}")
        cerrar_conexion(conexion)
        return []


# ============================================================
# FUNCIÓN DE PRUEBA
# ============================================================

def probar_conexion_loja():
    """
    Prueba la conexión al Nodo Loja y muestra información básica.
    """
    print("\n" + "="*60)
    print("PROBANDO CONEXIÓN AL NODO LOJA")
    print("="*60 + "\n")
    
    conexion = conectar_loja()
    
    if conexion:
        print("✓ Conexión exitosa")
        
        # Probar consulta simple
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM dbo.Cliente")
            total_clientes = cursor.fetchone()[0]
            print(f"✓ Total de clientes en base de datos: {total_clientes}")
            
            cursor.execute("SELECT COUNT(*) FROM dbo.Producto_Info")
            total_productos = cursor.fetchone()[0]
            print(f"✓ Total de productos en base de datos: {total_productos}")
            
            cursor.close()
        except Exception as e:
            print(f"✗ Error en consulta de prueba: {e}")
        
        cerrar_conexion(conexion)
    else:
        print("✗ No se pudo establecer conexión")
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    # Ejecutar prueba de conexión
    probar_conexion_loja()