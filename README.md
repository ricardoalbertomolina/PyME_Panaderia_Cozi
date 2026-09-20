# PyME_Panaderia_Cozi
Diseño e implementación de una aplicación de gestión para la PyME "Panadería Cozi", optimizando el inventario, la gestión de ventas y la reposición de stock.

**PROGRAMACIÓN Y BASE DE DATOS** - Módulo Programador  
**PROFESORES:** Enzo  
**CICLO LECTIVO:** 2026  

### INTEGRANTES Y ROLES:
* **Coordinador:** Rodriguez Sofia Belen
* **Modelo de datos:** Machado Rebeca Anahi
* **Interfaz:** Miranda Nicolas 
* **Acceso a datos:** Parra Alexander 
* **Validaciones:** Parra Alexander 
* **Documentación y pruebas:** Molina Ricardo

---

## 📦 ENTIDADES DEL SISTEMA

* **Producto:** Representa el catálogo y el control de inventario.
* **Venta:** Registro de cada transacción realizada.
* **Detalle_venta:** Entidad intermedia para permitir vender varios productos en una sola venta.
* **Cliente:** Registro de clientes recurrentes.
* **Proveedor:** Representa la reposición de stock de los productos finales.
* **Historial_Precio:** Entidad para guardar históricos de cambios en los precios.
* **Historial_Venta:** Permite guardar el registro de los estados de todas las ventas.

---

## 💻 INTERFAZ Y BOCETOS

**Bocetos de pantallas:** [Ver PDF en Google Drive](https://drive.google.com/file/d/1F0he--sNUQXeaUCiHJbi4hC0_SKS13Sk/view?usp=sharing)

**Breve explicación del funcionamiento:**
* **Pantalla dividida en dos:**
  * **Izquierda:** Menú con botones para moverse entre: Productos, Ventas, Clientes, Proveedores y Reportes.
  * **Derecha:** Muestra la pantalla del módulo en el que estés (ej. la lista de productos).
* **Pantalla de Productos:**
  * Tiene un título, un botón para agregar nuevo producto, una barra para buscar y un filtro por categoría.
  * Muestra una tabla con: Código, Producto, Stock y Precio.
  * Abajo tiene botones para Editar o Eliminar el producto que selecciones en la tabla.
* **Tecnología:** Se usa la librería **Tkinter** (Python).
  * La ventana principal tiene funciones para armar el menú, el panel de productos y cargar datos de prueba. Los demás botones por el momento imprimen mensajes en consola para probar su interactividad.

---

## 🗄️ MODELO DE BASE DE DATOS

Este documento contiene el Modelo Entidad-Relación, el Diccionario de Datos y el Script SQL (DDL) normalizados para SQLite.

### 1. Modelo Entidad-Relación (E-R)
*(Nota: GitHub renderiza este diagrama automáticamente)*

```mermaid
erDiagram
    CLIENTE ||--o{ VENTA : "Realiza"
    PROVEEDOR ||--o{ PRODUCTO : "Suministra"
    VENTA ||--|{ DETALLE_VENTA : "Contiene"
    VENTA ||--o{ HISTORIAL_VENTA : "Registra estados"
    PRODUCTO ||--o{ DETALLE_VENTA : "Aparece en"
    PRODUCTO ||--o{ HISTORIAL_PRECIO : "Registra cambios"

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