from conexion import obtener_conexion


def inser_user(Nombrecompleto, Cedula, Usuario, Contraseña, Correo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO login(Nombrecompleto, Cedula, Usuario, Contraseña, Correo) VALUES (%s,%s,%s, %s, %s)",
            (Nombrecompleto, Cedula, Usuario, Contraseña, Correo),
        )
        conexion.commit()
        conexion.close()

