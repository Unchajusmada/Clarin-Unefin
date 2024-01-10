from conexion import obtener_conexion


def inser_productos(nombre, descripcion, precio, numeroVendedor, correoVendedor):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO productos(nombre, descripcion, precio, numeroVendedor, correoVendedor) VALUES (%s,%s,%s, %s, %s)",
            (nombre, descripcion, precio, numeroVendedor, correoVendedor),
        )
        conexion.commit()
        conexion.close()


def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id_producto, nombre, descripcion, precio, numeroVendedor, correoVendedor, FROM productos WHERE id_producto = %s",
            (id,),
        )
        producto = cursor.fetchone()
    conexion.close()
    return producto

"""
def obtener_productos():
    conexion = obtener_conexion()
    juegos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio FROM juegos")
        juegos = cursor.fetchall()
    conexion.close()
    return juegos
    
"""