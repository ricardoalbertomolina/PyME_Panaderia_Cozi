# PyME_Panaderia_Cozi
Diseño e implementación de una aplicación de gestión para la PyME "Panadería Cozi", optimizando el inventario, la gestión de ventas y la reposición de stock.

**PROGRAMACIÓN Y BASE DE DATOS** - Módulo Programador  
**PROFESORES:** Maria Florencia Garcia Zavia  
Enzo Eduardo Bruno
  
**CICLO LECTIVO:** 2026  

### INTEGRANTES Y ROLES:
* **Coordinador:** Rodriguez Sofia Belen y Tula Emiliano 
* **Modelo de datos:** Machado Rebeca Anahi y Miranda Nicolas
* **Interfaz:** Puntano Ezequiel 
* **Acceso a datos:** Parra Alexander 
* **Validaciones:** Parra Alexander 
* **Documentación y pruebas:** Molina Ricardo y Tula Emiliano 

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

