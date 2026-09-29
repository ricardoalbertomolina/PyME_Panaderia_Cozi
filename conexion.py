import sqlite3
import os

def conectar():
    try:
        # Obtenemos la ruta absoluta de la carpeta donde está este archivo (conexion.py)
        # Que es: C:\Programacion\PyME_Panaderia_Cozi\Conexion
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Subimos UN solo nivel para salir de 'Conexion' y quedar en 'PyME_Panaderia_Cozi' 
        # (o dos niveles si tu base de datos está en C:\Programacion). 
        # Según tu captura de pantalla anterior, tu archivo .db está en C:\Programacion\sistema_ventas_panaderia_cozy.db
        # Por lo tanto, desde 'Conexion' necesitamos subir dos niveles (..) para llegar a C:\Programacion
        db_path = os.path.abspath(os.path.join(current_dir, "..", "..", "sistema_ventas_panaderia_cozy.db"))
        
        print(f"-> Conectando a la base de datos en: {db_path}")
        print(f"-> ¿El archivo de base de datos existe en esa ruta?: {os.path.exists(db_path)}")
        
        conexion = sqlite3.connect(db_path)
        conexion.execute("PRAGMA foreign_keys = ON;")
        
        # Rutina de seguridad para garantizar que las tablas existan siempre
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