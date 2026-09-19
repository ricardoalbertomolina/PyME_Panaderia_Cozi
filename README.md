# PyME_Panaderia_Cozi
Diseño e implementación de una aplicación de gestión para la optimización de inventario, ventas y trazabilidad productiva, con actualización de stock e ingresos. 

PROGRAMACIÓN Y BASE DE DATOS Módulo Programador 


PROFESORES: Enzo   


INTEGRANTES:
Molina Ricardo
Rodriguez Sofia Belen
Miranda Nicolas
Parra Garcia Alexander
Machado Rebeca Anahi


CICLO LECTIVO 2026


Distribución de Roles. 

Coordinador:  Rodriguez Sofia Belen
Modelo de datos: Rebeca Anahi Machado
Interfaz: Miranda Nicolas 
Acceso a datos: Parra Alexander 
Validaciones: Parra Alexander 
Documentación y pruebas: Molina Ricardo


ENTIDADES

Producto (Representa el catálogo y el control de inventario) 
Venta (Registro de cada transacción realizada) 
Detalle_venta (Entidad intermedia para permitir vender varios productos en una sola venta) 
Cliente (clientes recurrentes)
Proveedor (Representa la reposición de stock de los productos finales) 
Historal_Precio (entidad para guardar históricos de precios)

Bocetos de pantallas.

https://drive.google.com/file/d/1F0he--sNUQXeaUCiHJbi4hC0_SKS13Sk/view?usp=sharing 

BREVE EXPLICACION:

Pantalla dividida en dos:
Izquierda: Menú con botones para moverse entre: Productos, Ventas, Clientes, Proveedores y Reportes.

Derecha: Muestra la pantalla del módulo en el que estés (ej. la lista de productos).

Pantalla de Productos:
Tiene un título, un botón para agregar nuevo producto, una barra para buscar y un filtro por categoría.

Muestra una tabla con: Código, Producto, Stock y Precio.

Abajo tiene botones para Editar o Eliminar el producto que selecciones en la tabla.

Cómo funciona el código: Se usa Tkinter (Python).

La ventana principal tiene funciones para armar el menú, el panel de productos y cargar datos de prueba (tres productos inventados).

Los demás botones (Ventas, Clientes, etc.) todavía no tienen pantalla, solo imprimen un mensaje en consola para probar que funcionan.


            Modelo E-R normalizado 


 Modelo de Base de Datos: Sistema de Ventas

Este documento contiene el Modelo Entidad-Relación, el Diccionario de Datos y el Script SQL (DDL) normalizados y consistentes.


1. Modelo Entidad-Relación


    CLIENTE ||--o{ VENTA : "1:N (Realiza)"
    PROVEEDOR ||--o{ PRODUCTO : "1:N (Suministra)"
    VENTA ||--|{ DETALLE_VENTA : "1:N (Contiene)"
    VENTA ||--o{ HISTORIAL_VENTA : "1:N (Registra estados)"
    PRODUCTO ||--o{ DETALLE_VENTA : "1:N (Aparece en)"
    PRODUCTO ||--o{ HISTORIAL_PRECIO : "1:N (Registra cambios)"

    CLIENTE {
        int id_cliente PK
        string nombre
        string apellido
        string email
        string telefono
        string direccion
        timestamp fecha_registro
    }
    PROVEEDOR {
        int id_proveedor PK
        string nombre_proveedor
        string contacto
        string telefono
        string email
        
    }
    PRODUCTO {
        int id_producto PK
        int id_proveedor FK
        string nombre
        string categoria
        decimal precio_actual
        int stock
    }
    VENTA {
        int id_venta PK
        int id_cliente FK
        timestamp fecha_venta
        decimal total
    }
    DETALLE_VENTA {
        int id_detalle PK
        int id_venta FK
        int id_producto FK
        int cantidad
        decimal precio_unitario
        decimal subtotal
    }
    HISTORIAL_PRECIO {
        int id_historial_precio PK
        int id_producto FK
        decimal precio_anterior
        decimal precio_nuevo
        timestamp fecha_cambio
    }
    HISTORIAL_VENTA {
        int id_historial_venta PK
        int id_venta FK
        string estado_venta
        timestamp fecha_registro
        string observaciones
    }

Entidades:

Cliente
id_cliente (PK)
nombre
apellido
email
telefono
direccion
fecha_registro


PROVEEDOR 
id_proveedor (PK)
nombre_proveedor
telefono
email
contacto

PRODUCTO 
id_producto (PK)
id_proveedor (FK)
nombre
categoria
precio_actual
stock


HISTORIAL DE PRECIO
id_historial_precio (PK)
id_producto (FK)
precio_anterior
precio_nuevo
fecha_cambio
    

VENTA 
id_venta (PK)
id_cliente (FK)
fecha_venta
total

DETALLE_VENTA 
id_detalle (PK)
id_venta (FK)
id_producto (FK)
cantidad
precio_unitario
subtotal

HISTORIAL_VENTA
id_historial_venta (PK)
id_venta (FK)
estado_venta 
fecha_registro 
observaciones 

https://drive.google.com/file/d/1MaetbMFsVgB22h2jH0rOrxLUNFLBabis/view?usp=sharing


3. Script SQL (DDL)


-- 1. Tabla: Proveedor
CREATE TABLE proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    nombre_proveedor VARCHAR(150) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(150) UNIQUE
);

-- 2. Tabla: Cliente
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 3. Tabla: Producto
CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    id_proveedor INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    precio_actual DECIMAL(10,2) NOT NULL CHECK (precio_actual > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    CONSTRAINT fk_producto_proveedor 
        FOREIGN KEY (id_proveedor) 
        REFERENCES proveedor(id_proveedor) 
        ON DELETE RESTRICT
);

-- 4. Tabla: Historial de Precio
CREATE TABLE historial_precio (
    id_historial_precio SERIAL PRIMARY KEY,
    id_producto INT NOT NULL,
    precio_anterior DECIMAL(10,2) NOT NULL,
    precio_nuevo DECIMAL(10,2) NOT NULL,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_historial_producto 
        FOREIGN KEY (id_producto) 
        REFERENCES producto(id_producto) 
        ON DELETE CASCADE
);

-- 5. Tabla: Venta
CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total DECIMAL(12,2) DEFAULT 0.00 NOT NULL,
    CONSTRAINT fk_venta_cliente 
        FOREIGN KEY (id_cliente) 
        REFERENCES cliente(id_cliente) 
        ON DELETE RESTRICT
);

-- 6. Tabla: Detalle de Venta
CREATE TABLE detalle_venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
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
CREATE TABLE historial_venta (
    id_historial_venta SERIAL PRIMARY KEY,
    id_venta INT NOT NULL,
    estado_venta VARCHAR(50) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    observaciones TEXT,
    CONSTRAINT fk_historial_venta 
        FOREIGN KEY (id_venta) 
        REFERENCES venta(id_venta) 
        ON DELETE CASCADE
);