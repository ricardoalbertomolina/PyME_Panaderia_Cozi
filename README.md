# Sistema de gestion Panaderia Cozi
Diseño e implementación de una aplicación de gestión para la PyME "Panadería Cozi", optimizando el inventario, la gestión de ventas y la reposición de stock desarrollada para la Tecnicatura Superior en Desarrollo de Software del ISPC.

**PROGRAMACIÓN Y BASE DE DATOS** - **MÓDULO PROGRAMADOR**  

**PROFESORES:** 
- Maria Florencia Garcia Zavia  
- Enzo Eduardo Bruno
  
**CICLO LECTIVO:** 2026  

### INTEGRANTES Y ROLES:
* **Coordinador:** Rodriguez Sofia Belen 
* **Modelo de datos:** Machado Rebeca Anahi, Miranda Nicolas
* **Interfaz:** Puntano Ezequiel 
* **Acceso a datos:** Parra Alexander 
* **Validaciones:** Tula Emiliano
* **Documentación y pruebas:** Molina Ricardo

---

## 📦 ENTIDADES DEL SISTEMA

* **Producto:** Representa el catálogo y el control de inventario.
* **Venta:** Registro de cada transacción realizada.
* **Detalle_venta:** Entidad intermedia para permitir vender varios productos en una sola venta.
* **Cliente:** Registro de clientes recurrentes.
* **Proveedor:** Representa la reposición de stock de los productos finales.
* **Historial_Precio:** Entidad para guardar históricos de cambios en los precios.


---

## 💻 INTERFAZ Y BOCETOS

**Bocetos de pantallas:** [Enlace](https://drive.google.com/file/d/1Nx_9Q5KZE8eGQSQ4LkN_1-m_OVoIoPfT/view?usp=sharing "Enlace")

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
## Tecnologías

- Python 3
- tkinter y ttk
- Mysql

---
## Estructura

```text
PyME_Panaderia_Cozi/
├── interfaz/
│   ├── Interfaz_principal.py
│   ├── Login.py
├── Datos/
│   ├── acceso_a_datos.py
└── Conexion/
│   ├── conexion.py
├── main.py
├── README.md
```
