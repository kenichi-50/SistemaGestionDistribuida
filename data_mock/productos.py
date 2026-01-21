"""
data_mock/productos.py
======================
Datos de prueba (mock) para productos.
Simula datos que vendrían de la base de datos.

⚠️ TODO: Reemplazar por consultas SQL Server
Estos datos son temporales para probar la interfaz.

Autor: Sistema BDD Distribuida
Fecha: Enero 2026
"""


def obtener_productos_mock():
    """
    Retorna lista de productos de prueba.
    
    ⚠️ TODO: Reemplazar por consulta SQL Server:
    
    SELECT 
        p.idProducto as id,
        p.nombre,
        p.descripcion,
        p.codigo,
        p.precio,
        i.stock,
        i.fechaActualizacion as fecha_actualizacion
    FROM producto p
    LEFT JOIN inventario i ON p.idProducto = i.fkIdProducto
    WHERE i.fkIdTienda = ?  -- Filtrar por tienda del nodo
    ORDER BY p.nombre
    
    Returns:
        list: Lista de diccionarios con datos de productos
    """
    # TODO: Reemplazar por consulta SQL Server
    
    productos_mock = [
        {
            'id': 1,
            'nombre': 'Teclado Mecánico RGB',
            'descripcion': 'Teclado mecánico gaming con luces RGB personalizables',
            'codigo': 'TKL-RGB100',
            'precio': 45.99,
            'stock': 25,
            'fecha_actualizacion': '2026-01-07'
        },
        {
            'id': 2,
            'nombre': 'Mouse Inalámbrico Ergonómico',
            'descripcion': 'Mouse inalámbrico con diseño ergonómico',
            'codigo': 'MS-WL600',
            'precio': 29.99,
            'stock': 40,
            'fecha_actualizacion': '2026-01-07'
        },
        {
            'id': 3,
            'nombre': 'Monitor IPS 24" Full HD',
            'descripcion': 'Monitor profesional IPS 24 pulgadas',
            'codigo': 'MON-24FHD',
            'precio': 199.50,
            'stock': 10,
            'fecha_actualizacion': '2026-01-06'
        },
        {
            'id': 4,
            'nombre': 'Cuaderno Rayado 100 hojas A4',
            'descripcion': 'Cuaderno universitario rayado',
            'codigo': 'CUA-100AA',
            'precio': 2.75,
            'stock': 150,
            'fecha_actualizacion': '2026-01-05'
        },
        {
            'id': 5,
            'nombre': 'Silla Gamer Reclinable Negra',
            'descripcion': 'Silla gaming ergonómica con reclinación 180°',
            'codigo': 'SLL-GMR200',
            'precio': 179.99,
            'stock': 8,
            'fecha_actualizacion': '2026-01-05'
        },
        {
            'id': 6,
            'nombre': 'Laptop Lenovo ThinkPad',
            'descripcion': 'Laptop empresarial Core i5, 8GB RAM, 256GB SSD',
            'codigo': 'LAP-THNK-450',
            'precio': 899.00,
            'stock': 5,
            'fecha_actualizacion': '2026-01-04'
        },
    ]
    
    return productos_mock