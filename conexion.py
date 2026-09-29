import sqlite3
import os

def conectar():
    try:
        # Ruta absoluta exacta al archivo en la carpeta Programacion
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "..", "..", "sistema_ventas_panaderia_cozy.db")
        db_path = os.path.normpath(db_path)
        
        print(f"Conectando a la base de datos en: {db_path}")
        
        conexion = sqlite3.connect(db_path)
        conexion.execute("PRAGMA foreign_keys = ON;")
        
        # RUTINA DE SEGURIDAD AUTOMÁTICA:
        # Si las tablas no existen en este archivo, las crea automáticamente para evitar el error.
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedor (
                id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_empresa TEXT NOT NULL,
                contacto TEXT,
                telefono TEXT,
                email TEXT
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producto (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                id_proveedor INTEGER,
                nombre TEXT NOT NULL,
                categoria TEXT,
                precio_actual REAL,
                stock INTEGER,
                FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                direccion TEXT
            );
        """)
        
        conexion.commit()
        return conexion
        
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None