import sqlite3
import os

def conectar():
    try:
        # Apuntamos directamente y sin dudas a la ruta exacta donde está tu archivo en la PC
        db_path = r"C:\Programacion\sistema_ventas_panaderia_cozy.db"
        
        print(f"-> CONECTANDO FIJO A: {db_path}")
        print(f"-> ¿EL ARCHIVO EXISTE?: {os.path.exists(db_path)}")
        
        conexion = sqlite3.connect(db_path)
        conexion.execute("PRAGMA foreign_keys = ON;")
        
        # Forzamos la creación de la tabla producto por si acaso
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producto (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                id_proveedor INTEGER,
                nombre TEXT NOT NULL,
                categoria TEXT,
                precio_actual REAL,
                stock INTEGER
            );
        """)
        conexion.commit()
        
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None