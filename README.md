# PyME_Panaderia_Cozi
Diseño e implementación de una aplicación de gestión para la optimización de inventario, ventas y trazabilidad productiva, con actualización de stock e ingresos. 
MODULO PROGRAMACION Y BASE DE DATOS
PROFESORES

PyME Panaderia Cozi

INTEGRANTES
RICARDO ALBERTO MOLINA
ALEXANDER 
NICOLAS MIRANDA
SOFIA RODRIGUEZ
REBECA ANAHI MACHADO

CICLO LECTIVO 2026



Evidencia 5: 

            Modelo E-R normalizado 
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
PRODUCTO 
id_producto (PK)
id_proveedor (FK)
nombre
categoria
precio_actual
stock
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
id_venta 
estado_venta 
fecha_registro 
observaciones 

https://drive.google.com/file/d/1MaetbMFsVgB22h2jH0rOrxLUNFLBabis/view?usp=sharing


MODELO ENTIDAD RELACION

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
    }
    PROVEEDOR {
        int id_proveedor PK
        string nombre_empresa
        string contacto
    }
    PRODUCTO {
        int id_producto PK
        int id_proveedor FK
        string nombre
        decimal precio_actual
    }
    VENTA {
        int id_venta PK
        int id_cliente FK
        timestamp fecha_venta
    }
    DETALLE_VENTA {
        int id_detalle PK
        int id_venta FK
        int id_producto FK
        int cantidad
        decimal subtotal
    }
    HISTORIAL_PRECIO {
        int id_historial PK
        int id_producto FK
        decimal precio_anterior
        decimal precio_nuevo
    }
    HISTORIAL_VENTA {
        int id_historial_venta PK
        int id_venta FK
        string estado_venta
        timestamp fecha_registro


1. cliente
Almacena la información de los compradores.        
Campo,               Tipo       Restricciones         Descripción
id_cliente,SERIAL    INT,"PK    Auto-incremental       Identificador unico del cliente.
nombre               VARCHAR(100)    NN                Nombre(s) del cliente.
apellido             VARCHAR(100)    NN                Apellido(s) del cliente.
email                VARCHAR(150)    UQ                Correo electrónico de contacto.
telefono             VARCHAR(20)     -                 Número de teléfono.
direccion            TEXT            -                 Dirección física de envío o facturación.
fecha_registro       DATE        NN,Default:CURRENT    Fecha de registro en el sistema.


2. PROVEEDOR
Campo               Tipo              Restricciones               Descripción
id_proveedor      SERIAL/INT      "PK, Auto-incremental"       Identificador único del proveedor.
nombre_empresa    VARCHAR(150)         NN                      Razón social o nombre comercial.
contacto          VARCHAR(100)         -                       Nombre de la persona de contacto.
telefono          VARCHAR(20)          -                       Teléfono del proveedor.
email             VARCHAR(150)         UQ                      Correo electrónico corporativo.

3. PRODUCTO
Campo               Tipo            Restricciones              Descripción
id_producto         SERIAL         INT,"PK, Auto-incremental     Identificador único del producto.
id_proveedor         INT,"FK        NN                           Referencia al proveedor (Tabla: proveedor).
nombre              VARCHAR(150)    NN                           Nombre del producto.
descripcion         TEXT             -                           Detalles y características.
precio_actual       DECIMAL(10,2)   NN, Check > 0"               Precio de venta vigente.
stock               INT             NN, Check >= 0"              Cantidad de unidades disponibles.

4. HISTORIAL_VENTA
Campo                 Tipo             Restricciones            Descripción
id_historial         SERIAL/INT,PK   Auto-incremental     Identificador único del registro.
id_venta             INT                FK,NN             Referencia a la venta (Tabla: venta).
estado_venta        VARCHAR(50)         NN                Estado asignado.
fecha_registro      DATE              NN,Default:CURRENT   Fecha y hora del cambio de estado.
observaciones        TEXT           -                        Notas adicionales.

5. VENTA
Campo               Tipo            Restricciones                   Descripción
id_venta,       SERIAL/INT,"PK"    Auto-incremental         Identificador único de la transacción.
id_cliente       INT,"FK               NN                   Referencia al cliente (Tabla: cliente).
fecha_venta      DATE                  NN,Default:CURRENT   Fecha y hora de la venta.
total           DECIMAL(12,2)          NN, Default: 0.00"   Monto total final.

6. DETALLE_VENTA
Campo               Tipo                 Restricciones               Descripción
id_detalle      SERIAL/INT,        "PK" Auto-incremental"     Identificador de la línea de detalle.
id_venta          INT                "FK, NN"                 Referencia a la venta (Tabla: venta).
id_producto       INT                "FK, NN"             Referencia al producto (Tabla: producto).
cantidad          INT                  "NN, Check > 0"         Unidades compradas.
precio_unitario  DECIMAL(10,2)        "NN, Check > 0"          Precio al momento de la venta.
subtotal,        DECIMAL(12,2)         "NN,cantidad *"         precio_unitario.

-- 1. Tabla: Proveedor
CREATE TABLE proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(150) NOT NULL,
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
    descripcion TEXT,
    precio_actual DECIMAL(10,2) NOT NULL CHECK (precio_actual > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    CONSTRAINT fk_producto_proveedor 
        FOREIGN KEY (id_proveedor) 
        REFERENCES proveedor(id_proveedor) 
        ON DELETE RESTRICT
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

