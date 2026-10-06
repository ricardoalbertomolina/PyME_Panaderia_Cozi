import sqlite3

def conectar():
    try:
        conexion = sqlite3.connect('sistema_ventas_panaderia_cozy.db')
        cursor = conexion.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
