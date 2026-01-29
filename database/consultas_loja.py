"""
database/consultas_loja.py
===========================
Consultas SQL para el Nodo de Operación (Loja).

Funcionalidades:
- CRUD de Clientes
- Consulta de Productos (SOLO LECTURA)
- CRUD de Empleados (solo Loja)
- CRUD de Ventas (solo Loja)
- Consulta de Inventario (solo Loja)

IMPORTANTE: NO tiene acceso a Tiendas

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from database.conexion import conectar_loja, cerrar_conexion
import pyodbc


# ============================================================
# CRUD - CLIENTES (Loja)
# ============================================================

def obtener_clientes_loja():
    """
    Obtiene todos los clientes desde Loja.
    Los clientes se replican, por lo que ambos nodos los ven.
    
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
                'direccion': row[2] if row[2] else '',
                'telefono': row[3] if row[3] else '',
                'correo': row[4] if row[4] else '',
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
    Inserta un nuevo cliente en Loja.
    
    Args:
        nombre (str): Nombre del cliente
        direccion (str): Dirección
        telefono (str): Teléfono
        correo (str): Correo electrónico
        
    Returns:
        bool: True si se insertó correctamente
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
        
        print(f"✓ Cliente '{nombre}' insertado correctamente en Loja")
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
    Actualiza un cliente existente en Loja.
    
    Args:
        id_cliente (int): ID del cliente
        nombre (str): Nombre
        direccion (str): Dirección
        telefono (str): Teléfono
        correo (str): Correo
        
    Returns:
        bool: True si se actualizó correctamente
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
    Elimina un cliente de Loja.
    
    Args:
        id_cliente (int): ID del cliente
        
    Returns:
        bool: True si se eliminó correctamente
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
# CONSULTA - PRODUCTOS (SOLO LECTURA en Loja)
# ============================================================

def obtener_productos_loja():
    """
    Obtiene todos los productos (SOLO LECTURA).
    
    Los productos son gestionados desde Quito.
    Loja solo puede consultarlos para ventas.
    
    Returns:
        list: Lista de diccionarios con datos de productos
    """
    conexion = conectar_loja()
    if not conexion:
        return []


def obtener_productos_loja_por_tienda(id_tienda=3):
    """
    Retorna productos disponibles en la sucursal de Loja indicada, con stock.
    """
    conexion = conectar_loja()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT 
                p.id_producto,
                p.nombre,
                p.precio_cents,
                i.stock
            FROM dbo.Inventario_Loja i
            INNER JOIN dbo.Producto_Info p ON p.id_producto = i.fkIdProducto
            WHERE i.fkIdTienda = ?
            ORDER BY p.nombre
            """,
            (id_tienda,)
        )
        productos = []
        for row in cursor.fetchall():
            productos.append({
                'id': row[0],
                'nombre': row[1],
                'precio': (row[2] or 0) / 100.0,
                'stock': row[3] or 0
            })
        cursor.close()
        cerrar_conexion(conexion)
        return productos
    except pyodbc.Error as e:
        print(f"✗ Error al obtener productos por tienda (Loja): {e}")
        cerrar_conexion(conexion)
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
                'precio': row[5] / 100.0 if row[5] else 0.0,
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
# CRUD - EMPLEADOS (Solo empleados de Loja)
# ============================================================

def obtener_empleados_loja():
    """
    Obtiene los empleados de Loja (fkIdTienda = 3).
    
    Returns:
        list: Lista de diccionarios con datos de empleados
    """
    conexion = conectar_loja()
    if not conexion:
        return []


def obtener_empleados_loja_por_tienda(id_tienda=3):
    """
    Obtiene empleados de Loja filtrados por sucursal.
    """
    conexion = conectar_loja()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT 
                e.idEmpleado,
                e.nombre,
                e.telefono,
                e.cargo,
                e.fechaContratacion,
                e.fkIdTienda
            FROM dbo.Vista_Empleados_Global e
            WHERE e.fkIdTienda = ?
            ORDER BY e.nombre
            """,
            (id_tienda,)
        )
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
        print(f"✗ Error al obtener empleados por tienda (Loja): {e}")
        cerrar_conexion(conexion)
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
            FROM dbo.Vista_Empleados_Global e
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


def insertar_empleado_loja(nombre, telefono, cargo, id_tienda=3):
    """
    Inserta un nuevo empleado en Loja.
    
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
        
        print(f"✓ Empleado '{nombre}' insertado correctamente en Loja")
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
    Actualiza un empleado existente en Loja.
    
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
    Elimina un empleado de Loja.
    
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
# CRUD - VENTAS (Solo ventas de Loja)
# ============================================================

def obtener_ventas_loja():
    """
    Obtiene las ventas de Loja (fkIdTienda = 3).
    
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
                'total': row[2] / 100.0 if row[2] else 0.0,
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
    Inserta una nueva venta con detalles en Loja.
    
    Realiza múltiples operaciones:
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
        
        # 1. Insertar cabecera de venta (incluye fechaVenta) y obtener id
        cursor.execute(
            """
            INSERT INTO dbo.Venta_Loja (fechaVenta, totalCents, fkIdCliente, fkIdEmpleado, fkIdTienda)
            OUTPUT INSERTED.idVenta
            VALUES (CONVERT(date, GETDATE()), ?, ?, ?, ?)
            """,
            (total_cents, id_cliente, id_empleado, id_tienda)
        )

        id_venta = int(cursor.fetchone()[0])
        
        cursor.execute("SET XACT_ABORT ON")

        # 2. Insertar detalles de venta
        query_detalle = """
            INSERT INTO dbo.DetalleVenta_Loja (
                fkIdVenta,
                nLineald,
                fkIdProducto,
                cantidad,
                precioUnitCents,
                fkIdTienda
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        for idx, detalle in enumerate(detalles, start=1):
            cursor.execute(
                query_detalle,
                (
                    int(id_venta),
                    idx,
                    detalle['id_producto'],
                    detalle['cantidad'],
                    int(detalle['precio_unitario'] * 100),
                    id_tienda
                )
            )

        # 3. Actualizar inventario (restar stock)
        for d in detalles:
            # Prevenir stock negativo en DB
            cursor.execute(
                """
                UPDATE dbo.Inventario_Loja
                SET stock = stock - ?,
                    fechaActualizacion = GETDATE()
                WHERE fkIdProducto = ? AND fkIdTienda = ? AND stock >= ?
                """,
                (d['cantidad'], d['id_producto'], id_tienda, d['cantidad'])
            )
            if cursor.rowcount == 0:
                raise pyodbc.Error("Stock insuficiente para producto en sucursal (Loja)")

        conexion.commit()
        cursor.close()
        cerrar_conexion(conexion)

        print(f"✓ Venta {id_venta} registrada correctamente")
        return id_venta

    except pyodbc.Error as e:
        print(f"✗ Error al insertar venta: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return None

def obtener_detalle_venta_loja(id_venta):
    """
    Obtiene el detalle de una venta específica de Loja.
    
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
                dv.nLineald,
                dv.fkIdProducto,
                p.nombre as nombre_producto,
                p.precio_cents
            FROM dbo.DetalleVenta_Loja dv
            LEFT JOIN dbo.Producto_Info p ON dv.fkIdProducto = p.id_producto
            WHERE dv.fkIdVenta = ?
            ORDER BY dv.nLineald
        """
        cursor.execute(query, (id_venta,))
        resultados = cursor.fetchall()
        
        detalles = []
        for row in resultados:
            detalles.append({
                'id_venta': row[0],
                'linea_id': row[1],
                'id_producto': row[2],
                'nombre_producto': row[3] if row[3] else 'N/A',
                'precio_unitario': row[4] / 100.0 if row[4] else 0.0
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return detalles
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener detalle de venta: {e}")
        cerrar_conexion(conexion)
        return []


# ============================================================
# CONSULTA - INVENTARIO (Solo inventario de Loja)
# ============================================================

def obtener_inventario_loja():
    """
    Obtiene el inventario de Loja (fkIdTienda = 3).
    
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
                i.fechaActualizacion,
                p.nombre as nombre_producto,
                p.stock_minimo
            FROM dbo.Inventario_Loja i
            LEFT JOIN dbo.Producto_Info p ON i.fkIdProducto = p.id_producto
            ORDER BY p.nombre
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        inventario = []
        for row in resultados:
            inventario.append({
                'id_tienda': row[0],
                'id_producto': row[1],
                'stock': row[2],
                'fecha_actualizacion': str(row[3]) if row[3] else '',
                'nombre_producto': row[4] if row[4] else 'N/A',
                'stock_minimo': row[5] if row[5] else 0
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return inventario
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener inventario: {e}")
        cerrar_conexion(conexion)
        return []


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def verificar_stock_disponible(id_producto, cantidad_solicitada):
    """
    Verifica si hay stock disponible de un producto.
    
    Args:
        id_producto (int): ID del producto
        cantidad_solicitada (int): Cantidad que se desea vender
        
    Returns:
        tuple: (bool, int) - (tiene_stock, stock_actual)
    """
    conexion = conectar_loja()
    if not conexion:
        return (False, 0)
    
    try:
        cursor = conexion.cursor()
        query = """
            SELECT stock
            FROM dbo.Inventario_Loja
            WHERE fkIdProducto = ? AND fkIdTienda = 3
        """
        cursor.execute(query, (id_producto,))
        resultado = cursor.fetchone()
        
        cursor.close()
        cerrar_conexion(conexion)
        
        if resultado:
            stock_actual = resultado[0]
            tiene_stock = stock_actual >= cantidad_solicitada
            return (tiene_stock, stock_actual)
        
        return (False, 0)
        
    except pyodbc.Error as e:
        print(f"✗ Error al verificar stock: {e}")
        cerrar_conexion(conexion)
        return (False, 0)