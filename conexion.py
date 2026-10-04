import sqlite3
import os

def conectar():
    # Usamos la ruta EXACTA que muestra tu DB Browser en la barra superior
    db_path = r"C:\Programacion\sistema_ventas_panaderia_cozy.db"
    
   
    if not os.path.exists(db_path):
        print(f"¡ERROR FATAL! No se encuentra la base de datos en: {db_path}")
        return None

    try:
        conexion = sqlite3.connect(db_path)
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar: {e}")
        return None