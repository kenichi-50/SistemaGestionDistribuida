from database.conexion import conectar_loja

def obtener_inventario_loja():
    conexion = conectar_loja()
    if not conexion:
        return []

    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            fkIdTienda,
            fkIdProducto,
            stock,
            fechaActualizacion
        FROM Inventario_Loja
    """)

    datos = cursor.fetchall()
    conexion.close()
    return datos
