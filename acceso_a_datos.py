from conexion import conectar

def obtener_productos():
    """Consulta y devuelve todos los productos de la base de datos."""
    conexion = conectar()
    productos = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_producto, nombre, categoria, stock, precio_actual FROM producto")
            productos = cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
        finally:
            conexion.close()
    return productos

def obtener_clientes():
    """Consulta y devuelve todos los clientes de la base de datos."""
    conexion = conectar()
    clientes = []
    if conexion:
        try:
            cursor = conexion.cursor()
            # Seleccionamos Nombre, Apellido, Email, Teléfono y Dirección
            cursor.execute("SELECT nombre, apellido, email, telefono, direccion FROM cliente")
            clientes = cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
        finally:
            conexion.close()
    return clientes