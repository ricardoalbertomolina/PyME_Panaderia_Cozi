from Conexion.conexion import conectar

def obtener_productos():
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
    conexion = conectar()
    clientes = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, apellido, email, telefono, direccion FROM cliente")
            clientes = cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
        finally:
            conexion.close()
    return clientes