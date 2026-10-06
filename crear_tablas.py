from Conexion.conexion import conectar

def inicializar_bd():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS proveedor (
                id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_empresa VARCHAR(150) NOT NULL,
                contacto VARCHAR(100),
                telefono VARCHAR(20),
                email VARCHAR(150) UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE,
                telefono VARCHAR(20),
                direccion TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
        ''')
        conn.commit()
        conn.close()
        print("¡Base de datos y tablas inicializadas con éxito!")

if __name__ == "__main__":
    inicializar_bd()
