import sys
import os
directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)
import tkinter as tk
from tkinter import ttk, messagebox
from Datos.acceso_a_datos import ProductoDAO, ClienteDAO, ProveedorDAO, VentaDAO

class FormularioBase(tk.Toplevel):
    """Clase base para ventanas emergentes modales."""
    def __init__(self, parent, titulo, dimensiones):
        super().__init__(parent)
        self.title(titulo)
        self.geometry(dimensiones)
        self.configure(bg="#2c3e50")
        self.resizable(False, False)
        self.grab_set()

    def crear_label(self, texto, es_titulo=False):
        if es_titulo:
            tk.Label(
                self, text=texto, bg="#2c3e50", fg="#1abc9c", 
                font=("Arial", 14, "bold")
            ).pack(pady=10)
        else:
            tk.Label(
                self, text=texto, bg="#2c3e50", fg="white", 
                font=("Arial", 9, "bold")
            ).pack(anchor="w", padx=20)

    def crear_entrada(self):
        entry = tk.Entry(self, font=("Arial", 11), bd=0)
        entry.pack(pady=2, fill=tk.X, padx=20)
        return entry


class VentanaNuevaVenta(FormularioBase):
    """Ventana modal interactiva para realizar una venta (Carrito de compras)."""
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Procesar Nueva Venta", "650x550")
        self.al_guardar_callback = al_guardar_callback
        
        self.carrito = []
        self.lista_productos_cache = []
        self.lista_clientes_cache = []

        self._cargar_datos_combo()
        self._crear_interfaz_venta()

    def _cargar_datos_combo(self):
        """Carga clientes y productos utilizando las clases DAO."""
        try:
            self.lista_clientes_cache = ClienteDAO.obtener_todos()
            self.lista_productos_cache = ProductoDAO.obtener_todos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener datos iniciales: {e}")

    def _crear_interfaz_venta(self):
        self.crear_label("Registrar Venta", es_titulo=True)

        # Frame de Selección de Cliente
        frame_cliente = tk.Frame(self, bg="#2c3e50")
        frame_cliente.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(frame_cliente, text="Cliente:", bg="#2c3e50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.combo_cliente = ttk.Combobox(frame_cliente, state="readonly", font=("Arial", 10))
        
        # Formatear lista de clientes para el Combobox
        opciones_cli = [f"{c[0]} - {c[1]} {c[2]}" for c in self.lista_clientes_cache]
        self.combo_cliente['values'] = opciones_cli
        self.combo_cliente.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Frame de Selección de Producto y Cantidad
        frame_prod = tk.Frame(self, bg="#34495e", padx=10, pady=10)
        frame_prod.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(frame_prod, text="Producto:", bg="#34495e", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
        self.combo_producto = ttk.Combobox(frame_prod, state="readonly", font=("Arial", 9), width=25)
        
        # Formatear lista de productos para el Combobox
        opciones_prod = [f"{p[0]} - {p[1]} (Stock: {p[3]})" for p in self.lista_productos_cache]
        self.combo_producto['values'] = opciones_prod
        self.combo_producto.grid(row=1, column=0, padx=5, pady=2)

        tk.Label(frame_prod, text="Cantidad:", bg="#34495e", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=1, sticky="w")
        self.entry_cantidad = tk.Entry(frame_prod, font=("Arial", 10), width=8)
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=1, column=1, padx=5, pady=2)

        btn_agregar_item = tk.Button(
            frame_prod, text="➕ Agregar Item", command=self._agregar_al_carrito,
            bg="#1abc9c", fg="white", font=("Arial", 9, "bold"), bd=0, padx=10, cursor="hand2"
        )
        btn_agregar_item.grid(row=1, column=2, padx=10, pady=2)

        # Tabla del Carrito
        frame_tabla_cart = tk.Frame(self, bg="white")
        frame_tabla_cart.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        self.tabla_cart = ttk.Treeview(frame_tabla_cart, columns=("prod", "precio", "cant", "subtotal"), show="headings", height=6)
        self.tabla_cart.heading("prod", text="Producto")
        self.tabla_cart.heading("precio", text="P. Unit")
        self.tabla_cart.heading("cant", text="Cant.")
        self.tabla_cart.heading("subtotal", text="Subtotal")

        self.tabla_cart.column("prod", width=220)
        self.tabla_cart.column("precio", width=80, anchor=tk.E)
        self.tabla_cart.column("cant", width=60, anchor=tk.CENTER)
        self.tabla_cart.column("subtotal", width=90, anchor=tk.E)
        self.tabla_cart.pack(fill=tk.BOTH, expand=True)

        # Pie con Total y Botón de Procesar
        frame_pie = tk.Frame(self, bg="#2c3e50")
        frame_pie.pack(fill=tk.X, padx=20, pady=10)

        self.lbl_total = tk.Label(frame_pie, text="Total: $0.00", bg="#2c3e50", fg="#1abc9c", font=("Arial", 14, "bold"))
        self.lbl_total.pack(side=tk.LEFT)

        tk.Button(
            frame_pie, text="✔ Finalizar Venta", command=self.guardar_venta,
            font=("Arial", 11, "bold"), bg="#27ae60", fg="white", bd=0, padx=15, pady=5, cursor="hand2"
        ).pack(side=tk.RIGHT)

    def _agregar_al_carrito(self):
        idx_prod = self.combo_producto.current()
        cant_str = self.entry_cantidad.get().strip()

        if idx_prod == -1:
            messagebox.showerror("Error", "Seleccione un producto válido.")
            return

        try:
            cantidad = int(cant_str)
            if cantidad <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un entero mayor a 0.")
            return

        prod_sel = self.lista_productos_cache[idx_prod]
        id_prod, nombre, cat, stock, precio = prod_sel[0], prod_sel[1], prod_sel[2], prod_sel[3], float(prod_sel[4])

        if cantidad > stock:
            messagebox.showerror("Stock Insuficiente", f"Solo hay {stock} unidades disponibles de {nombre}.")
            return

        subtotal = precio * cantidad
        
        self.carrito.append({
            "id_prod": id_prod,
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

        self._actualizar_vista_carrito()

    def _actualizar_vista_carrito(self):
        for item in self.tabla_cart.get_children():
            self.tabla_cart.delete(item)

        total = 0.0
        for item in self.carrito:
            total += item["subtotal"]
            self.tabla_cart.insert("", tk.END, values=(item["nombre"], f"${item['precio']:.2f}", item["cantidad"], f"${item['subtotal']:.2f}"))

        self.lbl_total.config(text=f"Total: ${total:.2f}")

    def guardar_venta(self):
        idx_cli = self.combo_cliente.current()
        if idx_cli == -1:
            messagebox.showerror("Error", "Seleccione un cliente para la venta.")
            return

        if not self.carrito:
            messagebox.showerror("Error", "El carrito de compras está vacío.")
            return

        id_cliente = self.lista_clientes_cache[idx_cli][0]
        total_venta = sum(item["subtotal"] for item in self.carrito)

        try:
            # Procesamiento delegado al VentaDAO
            VentaDAO.procesar_venta(id_cliente, total_venta, self.carrito)
            messagebox.showinfo("Éxito", "Venta registrada e inventario actualizado con éxito.")
            self.destroy()
            self.al_guardar_callback("Ventas")
        except Exception as e:
            messagebox.showerror("Error de Transacción", f"No se pudo completar la venta: {e}")


class VentanaProducto(FormularioBase):
    """Ventana modal para registrar productos."""
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Registrar Nuevo Producto", "350x430")
        self.al_guardar_callback = al_guardar_callback
        self.lista_proveedores_cache = []

        self._cargar_proveedores()
        self._crear_interfaz()

    def _cargar_proveedores(self):
        """Carga la lista de proveedores desde la base de datos."""
        try:
            self.lista_proveedores_cache = ProveedorDAO.obtener_todos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores: {e}")

    def _crear_interfaz(self):
        self.crear_label("Nuevo Producto", es_titulo=True)

        # Seleccionar Proveedor mediante Combobox
        self.crear_label("Proveedor:")
        self.combo_prov = ttk.Combobox(self, state="readonly", font=("Arial", 10))
        opciones_prov = [f"{p[0]} - {p[1]}" for p in self.lista_proveedores_cache]
        self.combo_prov['values'] = opciones_prov
        self.combo_prov.pack(fill=tk.X, padx=20, pady=2)

        # Resto de campos
        self.crear_label("Nombre del Producto:")
        self.entry_nombre = self.crear_entrada()
        self.crear_label("Categoría:")
        self.entry_categoria = self.crear_entrada()
        self.crear_label("Precio Actual:")
        self.entry_precio = self.crear_entrada()
        self.crear_label("Stock Inicial:")
        self.entry_stock = self.crear_entrada()

        tk.Button(
            self, text="Guardar Producto", command=self.guardar,
            font=("Arial", 10, "bold"), bg="#1abc9c", fg="white", bd=0, height=2, cursor="hand2"
        ).pack(fill=tk.X, padx=20, pady=20)

    def guardar(self):
        idx_prov = self.combo_prov.current()
        nombre = self.entry_nombre.get().strip()
        categoria = self.entry_categoria.get().strip()
        precio = self.entry_precio.get().strip()
        stock = self.entry_stock.get().strip()

        if idx_prov == -1:
            messagebox.showerror("Error", "Por favor seleccione un proveedor de la lista.")
            return

        if not (nombre and precio and stock):
            messagebox.showerror("Error", "Por favor completa los campos obligatorios.")
            return

        try:
            p_val = float(precio)
            s_val = int(stock)
            if p_val < 0 or s_val < 0:
                raise ValueError("Valores negativos")

            # Obtener el ID del proveedor desde la lista guardada en caché
            id_prov = self.lista_proveedores_cache[idx_prov][0]

            ProductoDAO.guardar(id_prov, nombre, categoria, p_val, s_val)

            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            self.destroy()
            self.al_guardar_callback("Productos")
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos mayores o iguales a 0.")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar: {e}")


class VentanaProveedor(FormularioBase):
    """Ventana modal para registrar proveedores."""
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Registrar Nuevo Proveedor", "350x360")
        self.al_guardar_callback = al_guardar_callback

        self.crear_label("Nuevo Proveedor", es_titulo=True)
        self.crear_label("Nombre Empresa:")
        self.entry_empresa = self.crear_entrada()
        self.crear_label("Contacto:")
        self.entry_contacto = self.crear_entrada()
        self.crear_label("Teléfono:")
        self.entry_telefono = self.crear_entrada()
        self.crear_label("Email:")
        self.entry_email = self.crear_entrada()

        tk.Button(
            self, text="Guardar Proveedor", command=self.guardar,
            font=("Arial", 10, "bold"), bg="#1abc9c", fg="white", bd=0, height=2, cursor="hand2"
        ).pack(fill=tk.X, padx=20, pady=20)

    def guardar(self):
        empresa = self.entry_empresa.get().strip()
        contacto = self.entry_contacto.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()

        if not empresa:
            messagebox.showerror("Error", "El nombre de la empresa es obligatorio.")
            return

        try:
            ProveedorDAO.guardar(empresa, contacto, telefono, email)

            messagebox.showinfo("Éxito", "Proveedor guardado correctamente.")
            self.destroy()
            self.al_guardar_callback("Proveedores")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar: {e}")

class VentanaCliente(FormularioBase):
    """Ventana modal para registrar un nuevo cliente."""
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Registrar Nuevo Cliente", "350x400")
        self.al_guardar_callback = al_guardar_callback

        self.crear_label("Nuevo Cliente", es_titulo=True)
        self.crear_label("Nombre:")
        self.entry_nombre = self.crear_entrada()
        self.crear_label("Apellido:")
        self.entry_apellido = self.crear_entrada()
        self.crear_label("Correo Electrónico:")
        self.entry_email = self.crear_entrada()
        self.crear_label("Teléfono:")
        self.entry_telefono = self.crear_entrada()
        self.crear_label("Dirección:")
        self.entry_direccion = self.crear_entrada()

        tk.Button(
            self, text="Guardar Cliente", command=self.guardar,
            font=("Arial", 10, "bold"), bg="#1abc9c", fg="white", bd=0, height=2, cursor="hand2"
        ).pack(fill=tk.X, padx=20, pady=20)

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()
        direccion = self.entry_direccion.get().strip()

        if not (nombre and apellido):
            messagebox.showerror("Error", "Nombre y Apellido son campos obligatorios.")
            return

        try:
            ClienteDAO.guardar(nombre, apellido, email, telefono, direccion)
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.destroy()
            self.al_guardar_callback("Clientes")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar: {e}")

class SistemaPanaderia:
    """Clase principal del Sistema."""
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ventas - Panadería Cozi")
        self.root.geometry("1050x550")
        self.root.configure(bg="#f4f6f7")

        self._configurar_estilos()
        self._crear_interfaz()
        self.cambiar_modulo("Productos")

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#34495e", foreground="white")
        style.configure("Treeview", font=("Arial", 10), rowheight=26)

    def _crear_interfaz(self):
        # Panel Lateral (Menú)
        frame_menu = tk.Frame(self.root, bg="#2c3e50", width=220)
        frame_menu.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_menu, text="PANADERÍA COZI", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12, "bold")).pack(pady=25)

        btn_estilo = {
            "font": ("Arial", 10, "bold"), "bg": "#34495e", "fg": "white", "bd": 0,
            "activebackground": "#1abc9c", "activeforeground": "white", "height": 2
        }

        modulos = [
            ("📦 Productos", "Productos"),
            ("🛒 Ventas", "Ventas"),
            ("👥 Clientes", "Clientes"),
            ("🚚 Proveedores", "Proveedores")
        ]

        for texto, nombre in modulos:
            tk.Button(
                frame_menu, text=texto, 
                command=lambda m=nombre: self.cambiar_modulo(m), 
                **btn_estilo
            ).pack(fill=tk.X, padx=15, pady=5)

        # Panel Principal
        frame_trabajo = tk.Frame(self.root, bg="#f4f6f7")
        frame_trabajo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Encabezado
        frame_superior = tk.Frame(frame_trabajo, bg="#f4f6f7")
        frame_superior.pack(fill=tk.X, padx=30, pady=20)

        self.label_titulo = tk.Label(frame_superior, text="", bg="#f4f6f7", fg="#2c3e50", font=("Arial", 18, "bold"))
        self.label_titulo.pack(side=tk.LEFT)

        self.frame_acciones = tk.Frame(frame_superior, bg="#f4f6f7")
        self.frame_acciones.pack(side=tk.RIGHT)

        # Contenedor de Tabla
        frame_tabla = tk.Frame(frame_trabajo, bg="white", bd=1, relief=tk.SOLID)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

        self.tabla_datos = ttk.Treeview(frame_tabla, show="headings")
        self.tabla_datos.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla_datos.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla_datos.configure(yscrollcommand=scrollbar.set)

    def cambiar_modulo(self, nombre_modulo):
        self.label_titulo.config(text=f"Módulo de {nombre_modulo}")

        for widget in self.frame_acciones.winfo_children():
            widget.destroy()
        for fila in self.tabla_datos.get_children():
            self.tabla_datos.delete(fila)

        if nombre_modulo == "Productos":
            self._cargar_modulo_productos()
        elif nombre_modulo == "Ventas":
            self._cargar_modulo_ventas()
        elif nombre_modulo == "Clientes":
            self._cargar_modulo_clientes()
        elif nombre_modulo == "Proveedores":
            self._cargar_modulo_proveedores()

    def _cargar_modulo_productos(self):
            # Botón para registrar producto
            btn_nuevo = tk.Button(
                self.frame_acciones, text="+ Nuevo Producto", 
                command=lambda: VentanaProducto(self.root, self.cambiar_modulo),
                font=("Arial", 10, "bold"), bg="#27ae60", fg="white", bd=0, padx=10, pady=5, cursor="hand2"
            )
            btn_nuevo.pack(side=tk.LEFT, padx=5)

            # Botón para eliminar producto
            btn_eliminar = tk.Button(
                self.frame_acciones, text="🗑 Eliminar Producto", 
                command=self._eliminar_producto,
                font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", bd=0, padx=10, pady=5, cursor="hand2"
            )
            btn_eliminar.pack(side=tk.LEFT, padx=5)

            # Configuración de columnas
            self.tabla_datos["columns"] = ("codigo", "nombre", "categoria", "stock", "precio")
            configuraciones = [
                ("codigo", "Código", 80, tk.CENTER),
                ("nombre", "Producto", 250, tk.W),
                ("categoria", "Categoría", 150, tk.W),
                ("stock", "Stock", 90, tk.CENTER),
                ("precio", "Precio", 110, tk.E)
            ]
            for col, head, width, align in configuraciones:
                self.tabla_datos.heading(col, text=head)
                self.tabla_datos.column(col, width=width, anchor=align)

            for prod in ProductoDAO.obtener_todos():
                self.tabla_datos.insert("", tk.END, values=prod)

    def _eliminar_producto(self):
            """Elimina el producto seleccionado en la tabla previa confirmación."""
            item_seleccionado = self.tabla_datos.selection()
            
            if not item_seleccionado:
                messagebox.showwarning("Atención", "Por favor, seleccione un producto de la tabla para eliminar.")
                return

            # Extraer el ID y Nombre del producto seleccionado
            valores = self.tabla_datos.item(item_seleccionado, "values")
            id_producto = valores[0]
            nombre_producto = valores[1]

            confirmar = messagebox.askyesno(
                "Confirmar Eliminación", 
                f"¿Está seguro de que desea eliminar el producto '{nombre_producto}' (Código: {id_producto})?"
            )

            if confirmar:
                try:
                    ProductoDAO.eliminar(id_producto)
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                    self.cambiar_modulo("Productos")  # Refrescar la tabla
                except Exception as e:
                    messagebox.showerror(
                        "Error de Base de Datos", 
                        f"No se pudo eliminar el producto. Si ya está registrado en alguna venta, la base de datos impedirá la eliminación.\nDetalle: {e}"
                    )

    def _cargar_modulo_ventas(self):
        btn_venta = tk.Button(
            self.frame_acciones, text="+ Procesar Venta", 
            command=lambda: VentanaNuevaVenta(self.root, self.cambiar_modulo),
            font=("Arial", 10, "bold"), bg="#27ae60", fg="white", bd=0, padx=10, pady=5, cursor="hand2"
        )
        btn_venta.pack(side=tk.LEFT)

        self.tabla_datos["columns"] = ("id_venta", "cliente", "fecha", "total")
        configuraciones = [
            ("id_venta", "Nº Venta", 90, tk.CENTER),
            ("cliente", "Cliente", 250, tk.W),
            ("fecha", "Fecha / Hora", 180, tk.CENTER),
            ("total", "Total ($)", 120, tk.E)
        ]
        for col, head, width, align in configuraciones:
            self.tabla_datos.heading(col, text=head)
            self.tabla_datos.column(col, width=width, anchor=align)

        try:
            ventas = VentaDAO.obtener_historial()
            for v in ventas:
                self.tabla_datos.insert("", tk.END, values=(v[0], v[1], v[2], f"${float(v[3]):.2f}"))
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las ventas: {e}")

    def _cargar_modulo_clientes(self):
        # Botón para agregar cliente
        btn_nuevo = tk.Button(
            self.frame_acciones, text="+ Nuevo Cliente", 
            command=lambda: VentanaCliente(self.root, self.cambiar_modulo),
            font=("Arial", 10, "bold"), bg="#27ae60", fg="white", bd=0, padx=10, pady=5, cursor="hand2"
        )
        btn_nuevo.pack(side=tk.LEFT, padx=5)

        # Botón para eliminar cliente
        btn_eliminar = tk.Button(
            self.frame_acciones, text="🗑 Eliminar Cliente", 
            command=self._eliminar_cliente,
            font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", bd=0, padx=10, pady=5, cursor="hand2"
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Configuración de columnas de la tabla
        self.tabla_datos["columns"] = ("id", "nombre", "apellido", "email", "telefono", "direccion")
        configuraciones = [
            ("id", "ID", 50, tk.CENTER),
            ("nombre", "Nombre", 120, tk.W),
            ("apellido", "Apellido", 120, tk.W),
            ("email", "Correo Electrónico", 180, tk.W),
            ("telefono", "Teléfono", 100, tk.CENTER),
            ("direccion", "Dirección", 180, tk.W)
        ]
        for col, head, width, align in configuraciones:
            self.tabla_datos.heading(col, text=head)
            self.tabla_datos.column(col, width=width, anchor=align)

        for cli in ClienteDAO.obtener_todos():
            self.tabla_datos.insert("", tk.END, values=cli)

    def _eliminar_cliente(self):
        """Elimina el cliente seleccionado en la tabla previa confirmación."""
        item_seleccionado = self.tabla_datos.selection()
        
        if not item_seleccionado:
            messagebox.showwarning("Atención", "Por favor, seleccione un cliente de la tabla para eliminar.")
            return

        # Obtener datos de la fila seleccionada
        valores = self.tabla_datos.item(item_seleccionado, "values")
        id_cliente = valores[0]
        nombre_completo = f"{valores[1]} {valores[2]}"

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar al cliente '{nombre_completo}' (ID: {id_cliente})?"
        )

        if confirmar:
            try:
                ClienteDAO.eliminar(id_cliente)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.cambiar_modulo("Clientes")  # Refrescar la tabla
            except Exception as e:
                messagebox.showerror(
                    "Error de Base de Datos", 
                    f"No se pudo eliminar el cliente. Si tiene ventas registradas, no se puede eliminar.\nDetalle: {e}"
                )

    def _cargar_modulo_proveedores(self):
            # Botón para registrar proveedor
            btn_nuevo = tk.Button(
                self.frame_acciones, text="+ Nuevo Proveedor", 
                command=lambda: VentanaProveedor(self.root, self.cambiar_modulo),
                font=("Arial", 10, "bold"), bg="#27ae60", fg="white", bd=0, padx=10, pady=5, cursor="hand2"
            )
            btn_nuevo.pack(side=tk.LEFT, padx=5)

            # Botón para eliminar proveedor
            btn_eliminar = tk.Button(
                self.frame_acciones, text="🗑 Eliminar Proveedor", 
                command=self._eliminar_proveedor,
                font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", bd=0, padx=10, pady=5, cursor="hand2"
            )
            btn_eliminar.pack(side=tk.LEFT, padx=5)

            # Configuración de columnas
            self.tabla_datos["columns"] = ("id", "empresa", "contacto", "telefono", "email")
            configuraciones = [
                ("id", "Código", 70, tk.CENTER),
                ("empresa", "Empresa", 200, tk.W),
                ("contacto", "Contacto", 150, tk.W),
                ("telefono", "Teléfono", 120, tk.CENTER),
                ("email", "Correo Electrónico", 200, tk.W)
            ]
            for col, head, width, align in configuraciones:
                self.tabla_datos.heading(col, text=head)
                self.tabla_datos.column(col, width=width, anchor=align)

            for prov in ProveedorDAO.obtener_todos():
                self.tabla_datos.insert("", tk.END, values=prov)

    def _eliminar_proveedor(self):
        """Elimina el proveedor seleccionado en la tabla previa confirmación."""
        item_seleccionado = self.tabla_datos.selection()
        
        if not item_seleccionado:
            messagebox.showwarning("Atención", "Por favor, seleccione un proveedor de la tabla para eliminar.")
            return

        # Extraer el ID y Nombre de Empresa de la fila elegida
        valores = self.tabla_datos.item(item_seleccionado, "values")
        id_proveedor = valores[0]
        empresa = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar al proveedor '{empresa}' (Código: {id_proveedor})?"
        )

        if confirmar:
            try:
                ProveedorDAO.eliminar(id_proveedor)
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                self.cambiar_modulo("Proveedores")  # Refrescar la tabla
            except Exception as e:
                messagebox.showerror(
                    "Error de Base de Datos", 
                    f"No se pudo eliminar el proveedor. Si tiene productos asociados, la base de datos impedirá la eliminación.\nDetalle: {e}"
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaPanaderia(root)
    root.mainloop()