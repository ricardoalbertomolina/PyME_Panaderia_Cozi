from Conexion.conexion import conectar

def inicializar_bd():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        
    
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        cursor.executescript('''
            -- 1. Tabla: Proveedor
            CREATE TABLE IF NOT EXISTS proveedor (
                id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_proveedor VARCHAR(150) NOT NULL,
                contacto VARCHAR(100),
                telefono VARCHAR(20),
                email VARCHAR(150) UNIQUE
            );

            -- 2. Tabla: Cliente
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE,
                telefono VARCHAR(20),
                direccion TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            );

            -- 3. Tabla: Producto
            CREATE TABLE IF NOT EXISTS producto (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                id_proveedor INTEGER NOT NULL,
                nombre VARCHAR(150) NOT NULL,
                categoria VARCHAR(100),
                precio_actual DECIMAL(10,2) NOT NULL CHECK (precio_actual > 0),
                stock INTEGER NOT NULL CHECK (stock >= 0),
                CONSTRAINT fk_producto_proveedor
                    FOREIGN KEY (id_proveedor)
                    REFERENCES proveedor(id_proveedor)
                    ON DELETE RESTRICT
            );

            -- 4. Tabla: Historial de Precio
            CREATE TABLE IF NOT EXISTS historial_precio (
                id_historial_precio INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                precio_anterior DECIMAL(10,2) NOT NULL,
                precio_nuevo DECIMAL(10,2) NOT NULL,
                fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                CONSTRAINT fk_historial_producto
                    FOREIGN KEY (id_producto)
                    REFERENCES producto(id_producto)
                    ON DELETE CASCADE
            );

            -- 5. Tabla: Venta
            CREATE TABLE IF NOT EXISTS venta (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                total DECIMAL(12,2) DEFAULT 0.00 NOT NULL,
                CONSTRAINT fk_venta_cliente
                    FOREIGN KEY (id_cliente)
                    REFERENCES cliente(id_cliente)
                    ON DELETE RESTRICT
            );

            -- 6. Tabla: Detalle de Venta
            CREATE TABLE IF NOT EXISTS detalle_venta (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario > 0),
                subtotal DECIMAL(12,2) NOT NULL,
                CONSTRAINT fk_detalle_venta
                    FOREIGN KEY (id_venta)
                    REFERENCES venta(id_venta)
                    ON DELETE CASCADE,
                CONSTRAINT fk_detalle_producto
                    FOREIGN KEY (id_producto)
                    REFERENCES producto(id_producto)
                    ON DELETE RESTRICT
            );

            -- 7. Tabla: Historial de Venta
            CREATE TABLE IF NOT EXISTS historial_venta (
                id_historial_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                estado_venta VARCHAR(50) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                observaciones TEXT,
                CONSTRAINT fk_historial_venta
                    FOREIGN KEY (id_venta)
                    REFERENCES venta(id_venta)
                    ON DELETE CASCADE
            );

            -- 8. Tabla: Categoria
            CREATE TABLE IF NOT EXISTS categoria (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT
            );
        ''')
        
        conexion.commit()
        conexion.close()
        print("Base de datos creada y actualizada exitosamente.")

if __name__ == "__main__":
    inicializar_bd()