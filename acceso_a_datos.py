#backend de la pagina de la panaderia
from conexion import conectar

def obtener_productos():
    """Consulta y devuelve todos los productos de nuestra base de datos."""
    conexion = conectar()
    productos = []
    if conexion:
        try:
            cursor = conexion.cursor()
            # Seleccionamos Código, Nombre, Categoría, Stock y Precio
            cursor.execute("SELECT id_producto, nombre, categoria, stock, precio_actual FROM producto")
            productos = cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
        finally:
            conexion.close()
    return productos