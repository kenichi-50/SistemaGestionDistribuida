"""
database/consultas_quito.py
============================
Consultas SQL para el Nodo de Gestión (Quito).

Funcionalidades:
- CRUD completo de Tiendas
- CRUD completo de Productos
- CRUD de Clientes
- CRUD de Empleados (solo Quito)
- CRUD de Ventas (solo Quito)
- Consulta de Inventario (solo Quito)

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""

from database.conexion import conectar_quito, cerrar_conexion
import pyodbc


# ============================================================
# CRUD - TIENDAS (Solo disponible en Quito)
# ============================================================

def obtener_tiendas_quito():
    conexion = conectar_quito()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                idTienda,
                nombreTienda,
                direccion,
                ciudad,
                telfContacto
            FROM dbo.Tienda
            ORDER BY nombreTienda
        """)

        filas = cursor.fetchall()
        tiendas = []

        for f in filas:
            tiendas.append({
                'id': f[0],
                'nombre': f[1],          # 👈 alias lógico
                'direccion': f[2],
                'ciudad': f[3],
                'telefono': f[4]         # 👈 alias lógico
            })

        cursor.close()
        cerrar_conexion(conexion)
        return tiendas

    except pyodbc.Error as e:
        print("✗ Error al obtener tiendas:", e)
        cerrar_conexion(conexion)
        return []

def insertar_tienda_quito(nombre, ciudad, direccion, telefono):
    conexion = conectar_quito()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO dbo.Tienda 
                (nombreTienda, ciudad, direccion, telfContacto)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, ciudad, direccion, telefono))
        conexion.commit()

        cursor.close()
        cerrar_conexion(conexion)
        print(f"✓ Tienda '{nombre}' insertada correctamente")
        return True

    except pyodbc.Error as e:
        print(f"✗ Error al insertar tienda: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def actualizar_tienda_quito(id_tienda, nombre, ciudad, direccion, telefono):
    conexion = conectar_quito()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        query = """
            UPDATE dbo.Tienda
            SET nombreTienda = ?,
                ciudad = ?,
                direccion = ?,
                telfContacto = ?
            WHERE idTienda = ?
        """
        cursor.execute(query, (nombre, ciudad, direccion, telefono, id_tienda))
        conexion.commit()

        cursor.close()
        cerrar_conexion(conexion)
        print(f"✓ Tienda ID {id_tienda} actualizada correctamente")
        return True

    except pyodbc.Error as e:
        print(f"✗ Error al actualizar tienda: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def eliminar_tienda_quito(id_tienda):
    """
    Elimina una tienda del sistema.
    
    Args:
        id_tienda (int): ID de la tienda
        
    Returns:
        bool: True si se eliminó correctamente
    """
    conexion = conectar_quito()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM dbo.Tienda WHERE idTienda = ?"
        cursor.execute(query, (id_tienda,))
        conexion.commit()
        
        print(f"✓ Tienda ID {id_tienda} eliminada correctamente")
        cursor.close()
        cerrar_conexion(conexion)
        return True
        
    except pyodbc.Error as e:
        print(f"✗ Error al eliminar tienda: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


# ============================================================
# CRUD - PRODUCTOS (Gestión completa desde Quito)
# ============================================================

def obtener_productos_quito():
    conexion = conectar_quito()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                id_producto,
                nombre,
                marca,
                modelo,
                categoria,
                precio_cents,
                stock_minimo,
                costo_logistico,
                margen_ganancia,
                clasificacion_planeacion
            FROM dbo.Vista_Detalle_Producto
            ORDER BY id_producto
        """)

        productos = []

        for f in cursor.fetchall():
            productos.append({
                'id': f[0],
                'nombre': f[1],
                'marca': f[2] or '',
                'modelo': f[3] or '',
                'categoria': f[4] or '',
                'precio': (f[5] or 0) / 100,
                'stock_minimo': f[6],
                'costo_logistico': f[7],
                'margen_porcentaje': f[8],
                'clasificacion_planeacion': f[9]
            })

        cursor.close()
        cerrar_conexion(conexion)
        return productos

    except Exception as e:
        print("✗ Error al obtener productos (Quito):", e)
        cerrar_conexion(conexion)
        return []


def obtener_productos_quito_por_tienda(id_tienda):
    """
    Retorna solo productos disponibles en la sucursal indicada (Inventario_Quito).
    Incluye precio desde Vista_Detalle_Producto.
    """
    conexion = conectar_quito()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT 
                v.id_producto,
                v.nombre,
                v.precio_cents,
                i.stock
            FROM dbo.Vista_Detalle_Producto v
            INNER JOIN dbo.Inventario_Quito i 
                ON i.fkIdProducto = v.id_producto
            WHERE i.fkIdTienda = ?
            ORDER BY v.id_producto
            """,
            (id_tienda,)
        )

        productos = []
        for f in cursor.fetchall():
            productos.append({
                'id': f[0],
                'nombre': f[1],
                'precio': (f[2] or 0) / 100,
                'stock': f[3]
            })

        cursor.close()
        cerrar_conexion(conexion)
        return productos

    except Exception as e:
        print("✗ Error al obtener productos por tienda (Quito):", e)
        cerrar_conexion(conexion)
        return []

    



def insertar_producto_quito(
    nombre, marca, modelo, categoria,
    precio, stock_minimo,
    costo_logistico, margen_ganancia, clasificacion
):
    conexion = conectar_quito()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()

        # 1️⃣ Obtener ID desde SEQUENCE
        cursor.execute("SELECT NEXT VALUE FOR dbo.seq_producto")
        id_producto = cursor.fetchone()[0]

        precio_cents = int(precio * 100)

        # 2️⃣ Insertar Producto_Info
        cursor.execute("""
            INSERT INTO Producto_Info (
                id_producto, nombre, marca, modelo,
                categoria, precio_cents, stock_minimo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            id_producto, nombre, marca, modelo,
            categoria, precio_cents, stock_minimo
        ))

        # 3️⃣ Insertar Producto_Contenido
        cursor.execute("""
            INSERT INTO Producto_Contenido (
                id_producto, costo_logistico,
                margen_ganancia, clasificacion_planeacion
            )
            VALUES (?, ?, ?, ?)
        """, (
            id_producto, costo_logistico,
            margen_ganancia, clasificacion
        ))

        conexion.commit()
        return True

    except Exception as e:
        print("Error producto:", e)
        conexion.rollback()
        return False


def actualizar_producto_quito(
    id_producto, nombre, marca, modelo, categoria,
    precio, stock_minimo,
    costo_logistico, margen_ganancia, clasificacion
):
    conexion = conectar_quito()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        precio_cents = int(precio * 100)

        # 1️⃣ Producto_Info
        cursor.execute("""
            UPDATE dbo.Producto_Info
            SET nombre = ?, marca = ?, modelo = ?, categoria = ?,
                precio_cents = ?, stock_minimo = ?
            WHERE id_producto = ?
        """, (
            nombre, marca, modelo, categoria,
            precio_cents, stock_minimo, id_producto
        ))

        # 2️⃣ Producto_Contenido
        cursor.execute("""
            UPDATE dbo.Producto_Contenido
            SET costo_logistico = ?,
                margen_ganancia = ?,
                clasificacion_planeacion = ?
            WHERE id_producto = ?
        """, (
            costo_logistico, margen_ganancia,
            clasificacion, id_producto
        ))

        conexion.commit()
        print(f"✓ Producto ID {id_producto} actualizado correctamente")

        cursor.close()
        cerrar_conexion(conexion)
        return True

    except Exception as e:
        print("✗ Error al actualizar producto:", e)
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def eliminar_producto_quito(id_producto):
    conexion = conectar_quito()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()

        # 0️⃣ Validar referencias: ventas e inventario
        # Bloquear si el producto tiene ventas registradas
        cursor.execute("""
            SELECT COUNT(*)
            FROM dbo.DetalleVenta_Quito
            WHERE fkIdProducto = ?
        """, (id_producto,))
        usadas_en_ventas = cursor.fetchone()[0]
        if usadas_en_ventas and int(usadas_en_ventas) > 0:
            print("✗ No se puede eliminar: el producto tiene ventas registradas en Quito.")
            cursor.close()
            cerrar_conexion(conexion)
            return False

        # Verificar stock en inventario
        cursor.execute("""
            SELECT ISNULL(SUM(stock), 0)
            FROM dbo.Inventario_Quito
            WHERE fkIdProducto = ?
        """, (id_producto,))
        stock_total = cursor.fetchone()[0] or 0
        if int(stock_total) > 0:
            print("✗ No se puede eliminar: aún existe stock en inventario de Quito.")
            cursor.close()
            cerrar_conexion(conexion)
            return False

        # 0.1️⃣ Eliminar filas de inventario (si existen con stock 0)
        cursor.execute("""
            DELETE FROM dbo.Inventario_Quito
            WHERE fkIdProducto = ?
        """, (id_producto,))

        # 1️⃣ Borrar Producto_Contenido
        cursor.execute("""
            DELETE FROM dbo.Producto_Contenido
            WHERE id_producto = ?
        """, (id_producto,))

        # 2️⃣ Borrar Producto_Info
        cursor.execute("""
            DELETE FROM dbo.Producto_Info
            WHERE id_producto = ?
        """, (id_producto,))

        conexion.commit()
        print(f"✓ Producto ID {id_producto} eliminado correctamente")

        cursor.close()
        cerrar_conexion(conexion)
        return True

    except Exception as e:
        print("✗ Error al eliminar producto:", e)
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


# ============================================================
# CRUD - CLIENTES (Quito)
# ============================================================

def obtener_clientes_quito():
    """
    Obtiene todos los clientes desde Quito.
    
    Returns:
        list: Lista de diccionarios con datos de clientes
    """
    conexion = conectar_quito()
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
                rowguid8
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
                'rowguid8': str(row[6]) if row[6] else ''
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return clientes
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener clientes: {e}")
        cerrar_conexion(conexion)
        return []


def insertar_cliente_quito(nombre, direccion, telefono, correo):
    """
    Inserta un nuevo cliente desde Quito.
    
    Args:
        nombre (str): Nombre del cliente
        direccion (str): Dirección
        telefono (str): Teléfono
        correo (str): Correo electrónico
        
    Returns:
        bool: True si se insertó correctamente
    """
    conexion = conectar_quito()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO dbo.Cliente (
                nombre, direccion, telefono, correo,
                fechaRegistro, rowguid8
            )
            VALUES (?, ?, ?, ?, CONVERT(date, GETDATE()), NEWID());
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


def actualizar_cliente_quito(id_cliente, nombre, direccion, telefono, correo):
    """
    Actualiza un cliente existente desde Quito.
    """
    conexion = conectar_quito()
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


def eliminar_cliente_quito(id_cliente):
    """
    Elimina un cliente desde Quito.
    """
    conexion = conectar_quito()
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
# CRUD - EMPLEADOS (Solo empleados de Quito)
# ============================================================

def obtener_empleados_quito():
    """
    Obtiene todos los empleados de Quito (todas las sucursales de Quito).
    """
    conexion = conectar_quito()
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
            FROM dbo.Empleado_Quito e
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


def obtener_empleados_quito_por_tienda(id_tienda):
    """
    Obtiene los empleados de Quito filtrados por sucursal (fkIdTienda).
    """
    conexion = conectar_quito()
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
            FROM dbo.Empleado_Quito e
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
        print(f"✗ Error al obtener empleados por tienda: {e}")
        cerrar_conexion(conexion)
        return []


def insertar_empleado_quito(nombre, telefono, cargo, id_tienda):
    """
    Inserta un nuevo empleado en Quito.
    
    Args:
        nombre (str): Nombre del empleado
        telefono (str): Teléfono
        cargo (str): Cargo
        id_tienda (int): ID de la tienda (1 o 2 para Quito)
        
    Returns:
        bool: True si se insertó correctamente
    """
    conexion = conectar_quito()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO dbo.Empleado_Quito (nombre, telefono, cargo, fkIdTienda)
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


def actualizar_empleado_quito(id_empleado, nombre, telefono, cargo):
    """
    Actualiza un empleado de Quito.
    """
    conexion = conectar_quito()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
            UPDATE dbo.Empleado_Quito
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


def eliminar_empleado_quito(id_empleado):
    """
    Elimina un empleado de Quito.
    """
    conexion = conectar_quito()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM dbo.Empleado_Quito WHERE idEmpleado = ?"
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
# CRUD - VENTAS (Solo ventas de Quito)
# ============================================================

def obtener_ventas_quito():
    """
    Obtiene las ventas de Quito (fkIdTienda = 1 o 2).
    """
    conexion = conectar_quito()
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
            FROM dbo.Venta_Quito v
            LEFT JOIN dbo.Cliente c ON v.fkIdCliente = c.idCliente
            WHERE v.fkIdTienda IN (1, 2)
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


def insertar_venta_quito(id_cliente, id_empleado, id_tienda, detalles):
    """
    Inserta una nueva venta con detalles en Quito.
    
    Args:
        id_cliente (int): ID del cliente
        id_empleado (int): ID del empleado
        id_tienda (int): ID de la tienda (1 o 2)
        detalles (list): Lista de dict con id_producto, cantidad, precio_unitario
    
    Returns:
        int: ID de la venta o None si falla
    """
    conexion = conectar_quito()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor()
        
        # Calcular total
        total_cents = sum(int(d['precio_unitario'] * 100) * d['cantidad'] for d in detalles)
        
        # Insertar venta (incluye fechaVenta NOT NULL) y devolver id generado
        # Usamos OUTPUT INSERTED.idVenta para que el propio INSERT retorne el ID
        query_venta = """
            INSERT INTO dbo.Venta_Quito (fechaVenta, totalCents, fkIdCliente, fkIdEmpleado, fkIdTienda)
            OUTPUT INSERTED.idVenta
            VALUES (CONVERT(date, GETDATE()), ?, ?, ?, ?)
        """
        cursor.execute(query_venta, (total_cents, id_cliente, id_empleado, id_tienda))
        id_venta = int(cursor.fetchone()[0])
        
        # Insertar detalles
        query_detalle = """
            INSERT INTO dbo.DetalleVenta_Quito (
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
        
        # Actualizar inventario con guardas (no permitir negativos)
        for detalle in detalles:
            cursor.execute(
                """
                UPDATE dbo.Inventario_Quito
                SET stock = stock - ?,
                    fechaActualizacion = GETDATE()
                WHERE fkIdTienda = ? AND fkIdProducto = ? AND stock >= ?
                """,
                (
                    detalle['cantidad'],
                    id_tienda,
                    detalle['id_producto'],
                    detalle['cantidad']
                )
            )
            if cursor.rowcount == 0:
                raise pyodbc.Error("Stock insuficiente para producto en sucursal")
        
        conexion.commit()
        cursor.close()
        cerrar_conexion(conexion)
        return int(id_venta)
        
    except pyodbc.Error as e:
        print(f"✗ Error al insertar venta: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        raise


def obtener_venta_quito_por_id(id_venta):
    """
    Obtiene la cabecera de una venta específica en Quito.
    """
    conexion = conectar_quito()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT idVenta, fechaVenta, totalCents, fkIdCliente, fkIdEmpleado, fkIdTienda
            FROM dbo.Venta_Quito WHERE idVenta = ?
            """,
            (id_venta,)
        )
        row = cursor.fetchone()
        cursor.close()
        cerrar_conexion(conexion)
        if not row:
            return None
        return {
            'id': row[0],
            'fecha': str(row[1]) if row[1] else '',
            'total': row[2] / 100.0 if row[2] else 0.0,
            'id_cliente': row[3],
            'id_empleado': row[4],
            'id_tienda': row[5],
        }
    except pyodbc.Error as e:
        print(f"✗ Error al obtener venta por ID (Quito): {e}")
        cerrar_conexion(conexion)
        return None


def eliminar_venta_quito(id_venta):
    """
    Elimina una venta y revierte el stock en Quito.
    """
    conexion = conectar_quito()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        # Obtener detalles y tienda
        cursor.execute(
            """
            SELECT dv.fkIdProducto, dv.cantidad, dv.fkIdTienda
            FROM dbo.DetalleVenta_Quito dv WHERE dv.fkIdVenta = ?
            """,
            (id_venta,)
        )
        detalles = cursor.fetchall()

        # Revertir inventario
        for pid, cantidad, id_tienda in detalles:
            cursor.execute(
                """
                UPDATE dbo.Inventario_Quito
                SET stock = stock + ?, fechaActualizacion = GETDATE()
                WHERE fkIdTienda = ? AND fkIdProducto = ?
                """,
                (cantidad, id_tienda, pid)
            )

        # Eliminar detalles y cabecera
        cursor.execute("DELETE FROM dbo.DetalleVenta_Quito WHERE fkIdVenta = ?", (id_venta,))
        cursor.execute("DELETE FROM dbo.Venta_Quito WHERE idVenta = ?", (id_venta,))
        conexion.commit()
        cursor.close()
        cerrar_conexion(conexion)
        return True
    except pyodbc.Error as e:
        print(f"✗ Error al eliminar venta (Quito): {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False


def actualizar_venta_quito(id_venta, id_cliente, id_empleado, detalles):
    """
    Actualiza cabecera y detalles de una venta en Quito, ajustando inventario.
    Mantiene la tienda original.
    """
    conexion = conectar_quito()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        # Obtener cabecera actual (incluye tienda)
        cursor.execute(
            "SELECT fkIdTienda FROM dbo.Venta_Quito WHERE idVenta = ?",
            (id_venta,)
        )
        row = cursor.fetchone()
        if not row:
            raise pyodbc.Error("Venta no encontrada")
        id_tienda = int(row[0])

        # Obtener detalles actuales para revertir inventario
        cursor.execute(
            """
            SELECT fkIdProducto, cantidad FROM dbo.DetalleVenta_Quito
            WHERE fkIdVenta = ?
            """,
            (id_venta,)
        )
        actuales = cursor.fetchall()
        for pid, cantidad in actuales:
            cursor.execute(
                """
                UPDATE dbo.Inventario_Quito
                SET stock = stock + ?, fechaActualizacion = GETDATE()
                WHERE fkIdTienda = ? AND fkIdProducto = ?
                """,
                (cantidad, id_tienda, pid)
            )

        # Eliminar detalles actuales
        cursor.execute("DELETE FROM dbo.DetalleVenta_Quito WHERE fkIdVenta = ?", (id_venta,))

        # Insertar nuevos detalles (con guardas de stock)
        total_cents = sum(int(d['precio_unitario'] * 100) * d['cantidad'] for d in detalles)
        for idx, detalle in enumerate(detalles, start=1):
            # Guardar con check de stock
            cursor.execute(
                """
                UPDATE dbo.Inventario_Quito
                SET stock = stock - ?, fechaActualizacion = GETDATE()
                WHERE fkIdTienda = ? AND fkIdProducto = ? AND stock >= ?
                """,
                (detalle['cantidad'], id_tienda, detalle['id_producto'], detalle['cantidad'])
            )
            if cursor.rowcount == 0:
                raise pyodbc.Error("Stock insuficiente al actualizar venta")
            # Insertar línea
            cursor.execute(
                """
                INSERT INTO dbo.DetalleVenta_Quito (
                    fkIdVenta, nLineald, fkIdProducto, cantidad, precioUnitCents, fkIdTienda
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    id_venta,
                    idx,
                    detalle['id_producto'],
                    detalle['cantidad'],
                    int(detalle['precio_unitario'] * 100),
                    id_tienda,
                )
            )

        # Actualizar cabecera
        cursor.execute(
            """
            UPDATE dbo.Venta_Quito
            SET fkIdCliente = ?, fkIdEmpleado = ?, totalCents = ?, fechaVenta = fechaVenta
            WHERE idVenta = ?
            """,
            (id_cliente, id_empleado, total_cents, id_venta)
        )

        conexion.commit()
        cursor.close()
        cerrar_conexion(conexion)
        return True
    except pyodbc.Error as e:
        print(f"✗ Error al actualizar venta (Quito): {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        return False
    
    try:
        cursor = conexion.cursor()
        
        # Calcular total
        total_cents = sum(int(d['precio_unitario'] * 100) * d['cantidad'] for d in detalles)
        
        # Insertar venta (incluye fechaVenta NOT NULL) y devolver id generado
        # Usamos OUTPUT INSERTED.idVenta para que el propio INSERT retorne el ID
        query_venta = """
            INSERT INTO dbo.Venta_Quito (fechaVenta, totalCents, fkIdCliente, fkIdEmpleado, fkIdTienda)
            OUTPUT INSERTED.idVenta
            VALUES (CONVERT(date, GETDATE()), ?, ?, ?, ?)
        """
        cursor.execute(query_venta, (total_cents, id_cliente, id_empleado, id_tienda))
        id_venta = int(cursor.fetchone()[0])
        
        # Insertar detalles
        query_detalle = """
            INSERT INTO dbo.DetalleVenta_Quito (
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
        
        # Actualizar inventario
        query_inventario = """
            UPDATE dbo.Inventario_Quito
            SET stock = stock - ?,
                fechaActualizacion = GETDATE()
            WHERE fkIdTienda = ? AND fkIdProducto = ?
        """
        for detalle in detalles:
            # Guardar stock en DB sin permitir negativos (concurrencia segura)
            cursor.execute(
                """
                UPDATE dbo.Inventario_Quito
                SET stock = stock - ?,
                    fechaActualizacion = GETDATE()
                WHERE fkIdTienda = ? AND fkIdProducto = ? AND stock >= ?
                """,
                (
                    detalle['cantidad'],
                    id_tienda,
                    detalle['id_producto'],
                    detalle['cantidad']
                )
            )
            if cursor.rowcount == 0:
                raise pyodbc.Error("Stock insuficiente para producto en sucursal")
        
        conexion.commit()
        print(f"✓ Venta ID {id_venta} registrada correctamente")
        
        cursor.close()
        cerrar_conexion(conexion)
        return int(id_venta)
        
    except pyodbc.Error as e:
        print(f"✗ Error al insertar venta: {e}")
        conexion.rollback()
        cerrar_conexion(conexion)
        raise


def obtener_detalle_venta_quito(id_venta):
    """
    Obtiene el detalle de una venta específica de Quito.
    """
    conexion = conectar_quito()
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
                dv.precioUnitCents,
                dv.cantidad
            FROM dbo.DetalleVenta_Quito dv
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
                'precio_unit_cents': row[4] if row[4] is not None else 0,
                'cantidad': row[5] if row[5] is not None else 1,
                'precio_unitario': (row[4] or 0) / 100.0
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return detalles
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener detalle de venta: {e}")
        cerrar_conexion(conexion)
        return []


# ============================================================
# CONSULTA - INVENTARIO (Solo inventario de Quito)
# ============================================================

def obtener_inventario_quito():
    """
    Obtiene el inventario de Quito (fkIdTienda = 1 o 2).
    
    Returns:
        list: Lista de diccionarios con el inventario
    """
    conexion = conectar_quito()
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
                p.nombre as nombre_producto
            FROM dbo.Inventario_Quito i
            LEFT JOIN dbo.Producto_Info p ON i.fkIdProducto = p.id_producto
            WHERE i.fkIdTienda IN (1, 2)
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
                'nombre_producto': row[4] if row[4] else 'N/A'
            })
        
        cursor.close()
        cerrar_conexion(conexion)
        return inventario
        
    except pyodbc.Error as e:
        print(f"✗ Error al obtener inventario: {e}")
        cerrar_conexion(conexion)
        return []


# ============================================================
# DEBUG - Esquema DetalleVenta_Quito
# ============================================================

def debug_detalle_columns_quito():
    """
    Imprime las columnas de la tabla DetalleVenta_Quito para verificar nombres.
    """
    conexion = conectar_quito()
    if not conexion:
        print("✗ No se pudo conectar a Quito")
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'DetalleVenta_Quito'
            ORDER BY ORDINAL_POSITION
        """)
        cols = [row[0] for row in cursor.fetchall()]
        print("✓ Columnas DetalleVenta_Quito:", ", ".join(cols))
        cursor.close()
        cerrar_conexion(conexion)
    except pyodbc.Error as e:
        print(f"✗ Error al consultar columnas de DetalleVenta_Quito: {e}")
        cerrar_conexion(conexion)