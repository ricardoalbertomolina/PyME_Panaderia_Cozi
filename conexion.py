import sqlite3

def conectar():
    try:
        # Apunta al archivo .db que está en la raíz de la carpeta del proyecto
        conexion = sqlite3.connect('sistema_ventas_panaderia_cozy.db')
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None