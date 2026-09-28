import sqlite3
import os

def conectar():
    try:
        # Obtenemos la ruta actual (carpeta Conexion), subimos dos niveles (..) para salir de PyME_Panaderia_Cozi y llegar a Programacion
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "..", "..", "sistema_ventas_panaderia_cozy.db")
        
        # Normalizamos la ruta para asegurarnos de que Windows la lea correctamente
        db_path = os.path.normpath(db_path)
        
        print(f"Conectando a la base de datos en: {db_path}")
        
        conexion = sqlite3.connect(db_path)
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion
        
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None