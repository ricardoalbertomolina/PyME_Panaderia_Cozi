import sys
import os
directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps, ImageTk
from Datos.acceso_a_datos import ProductoDAO, ClienteDAO, ProveedorDAO, VentaDAO

# ---------- Paleta (la misma del login) ----------
BG = "#eedeb8"              # fondo general
BG_MENU = "#e2cd9b"         # menú lateral (un tono más oscuro que el fondo)
MARRON = "#ac6d3c"          # botones y encabezados
MARRON_HOVER = "#8c5224"    # hover de botones del menú
MARRON_OSCURO = "#763e12"   # hover / módulo activo / títulos
TEXTO = "#3e3e3e"
ROJO = "#e74c3c"            # botones de eliminar
ROJO_HOVER = "#c0392b"

# ---------- Medidas ----------
RADIO = 14            # esquinas de inputs y botones
RADIO_CARD = 14       # esquinas de la tarjeta blanca de las tablas
ANCHO_SCROLL = 12     # ancho de la barra de scroll
SCROLL_MARGEN = 4     # espacio entre el encabezado marrón y el scroll

# ---------- Logo (Interfaz/img/logo.png) ----------
CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_LOGO = os.path.join(CARPETA, "img", "logo.png")
TAMANO_LOGO = (180, 72)  # (ancho máximo, alto máximo)

PLACEHOLDER_COMBO = "Seleccione..."

ctk.set_appearance_mode("light")


def cargar_logo():
    """Devuelve el logo como CTkImage (mantiene la proporción), o None si falla."""
    if not os.path.exists(RUTA_LOGO):
        return None
    try:
        img = Image.open(RUTA_LOGO).convert("RGBA")
        ancho, alto = img.size
        escala = min(TAMANO_LOGO[0] / ancho, TAMANO_LOGO[1] / alto)
        tamano = (max(1, int(ancho * escala)), max(1, int(alto * escala)))
        return ctk.CTkImage(light_image=img, dark_image=img, size=tamano)
    except Exception:
        return None


def configurar_estilos():
    """Estilo de la tabla (ttk) con la misma paleta."""
    style = ttk.Style()
    style.theme_use("clam")
    # Quita el borde fino que dibuja el Treeview alrededor de la tabla
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=MARRON,
                    foreground="white", relief="flat", padding=6)
    # Sin cambio de color al pasar el mouse, para que las esquinas redondeadas coincidan siempre
    style.map("Treeview.Heading", background=[("active", MARRON)])
    style.configure("Treeview", font=("Arial", 10), rowheight=28, background="white",
                    fieldbackground="white", foreground=TEXTO, borderwidth=0)
    style.map("Treeview", background=[("selected", MARRON)], foreground=[("selected", "white")])


def crear_combo(parent, opciones, **kwargs):
    """Lista desplegable con el estilo del login. Empieza con el texto 'Seleccione...'."""
    combo = ctk.CTkComboBox(
        parent, values=opciones, state="readonly", height=38, corner_radius=RADIO,
        border_width=0, fg_color="white", text_color="black",
        button_color=MARRON, button_hover_color=MARRON_OSCURO,
        dropdown_fg_color="white", dropdown_text_color="black", dropdown_hover_color=BG,
        font=("Arial", 14), dropdown_font=("Arial", 13), **kwargs
    )
    combo.set(PLACEHOLDER_COMBO)
    return combo


def indice_combo(combo, opciones):
    """Posición de la opción elegida en la lista, o -1 si no se eligió ninguna."""
    try:
        return opciones.index(combo.get())
    except ValueError:
        return -1


class TablaTarjeta:
    """Tabla (ttk.Treeview) dentro de una tarjeta blanca de esquinas redondeadas,
    con scroll de CustomTkinter y encabezado marrón con las esquinas exteriores redondeadas."""

    def __init__(self, parent, ventana):
        self.ventana = ventana
        try:
            self.escala = ctk.ScalingTracker.get_window_scaling(ventana)  # escala de pantalla (125%, 150%...)
        except Exception:
            self.escala = 1.0
        self.ancho_relleno = int(24 * self.escala)
        self.radio_px = max(8, round(RADIO_CARD * self.escala))

        self.frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=RADIO_CARD)

        # La tabla ocupa todo el ancho y llega hasta el borde de arriba, izquierda y derecha
        self.tabla = ttk.Treeview(self.frame, show="headings")
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))

        # El scroll va encima del borde derecho de la tabla, debajo del encabezado
        self.barra_scroll = tk.Frame(self.frame, bg="white", bd=0, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self.barra_scroll, orientation="vertical", width=ANCHO_SCROLL,
                                          command=self.tabla.yview, button_color=MARRON,
                                          button_hover_color=MARRON_OSCURO)
        self.scrollbar.pack(fill=tk.Y, expand=True)
        self.tabla.configure(yscrollcommand=self.scrollbar.set)

        self._crear_esquina_header("izquierda")
        self._crear_esquina_header("derecha")
        ventana.after(200, self._posicionar_scroll)
        ventana.after(800, self._posicionar_scroll)

    def _posicionar_scroll(self):
        """Mide el alto del encabezado marrón y hace que el scroll arranque justo debajo."""
        try:
            self.ventana.update_idletasks()
            alto = 0
            for y in range(0, 150):
                if self.tabla.identify("region", 20, y) not in ("heading", "separator"):
                    break
                alto = y + 1
            if alto < 10:
                alto = int(32 * self.escala)  # valor de respaldo si todavía no se pudo medir
            inicio = alto + SCROLL_MARGEN
            self.barra_scroll.place(in_=self.tabla, relx=1.0, x=-int(5 * self.escala), y=inicio, anchor="ne",
                                    width=int(ANCHO_SCROLL * self.escala) + 4, relheight=1.0,
                                    height=-(inicio + int(6 * self.escala)))
        except tk.TclError:
            pass  # la ventana se cerró antes de que se ejecutara

    def _crear_esquina_header(self, lado):
        """ttk no permite redondear los encabezados, así que se tapan las puntas con una pequeña
        imagen: del color del fondo afuera del arco y marrón adentro (suavizada con Pillow)."""
        S = self.radio_px * 8  # se dibuja grande y se reduce para que quede suave
        img = Image.new("RGB", (S * 2, S * 2), BG)
        ImageDraw.Draw(img).ellipse((0, 0, S * 2 - 1, S * 2 - 1), fill=MARRON)
        esquina = img.crop((0, 0, S, S)).resize((self.radio_px, self.radio_px), Image.LANCZOS)
        if lado == "derecha":
            esquina = ImageOps.mirror(esquina)
        foto = ImageTk.PhotoImage(esquina)
        etiqueta = tk.Label(self.frame, image=foto, bd=0, highlightthickness=0, bg=BG)
        etiqueta.image = foto  # evita que Python borre la imagen
        if lado == "izquierda":
            etiqueta.place(in_=self.tabla, x=0, y=0)
        else:
            etiqueta.place(in_=self.tabla, relx=1.0, x=0, y=0, anchor="ne")

    def configurar_columnas(self, configuraciones):
        """configuraciones: lista de (columna, encabezado, ancho, alineación).
        Agrega una columna de relleno a la derecha, donde va el scroll."""
        self.tabla["columns"] = tuple(c[0] for c in configuraciones) + ("_relleno",)
        for col, cabecera, ancho, alineacion in configuraciones:
            self.tabla.heading(col, text=cabecera)
            self.tabla.column(col, width=ancho, anchor=alineacion)
        self.tabla.heading("_relleno", text="")
        self.tabla.column("_relleno", width=self.ancho_relleno, minwidth=self.ancho_relleno, stretch=False)

    def limpiar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

    def insertar(self, valores):
        self.tabla.insert("", tk.END, values=valores)

    def valores_seleccionados(self):
        """Valores de la fila seleccionada, o None si no hay ninguna."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        return self.tabla.item(seleccion[0], "values")


class FormularioBase(ctk.CTkToplevel):
    """Clase base para ventanas emergentes modales."""
    def __init__(self, parent, titulo, dimensiones):
        super().__init__(parent)
        self.title(titulo)
        self.geometry(dimensiones)
        self.configure(fg_color=BG)
        self.resizable(False, False)
        self.transient(parent)
        self.after(150, self.grab_set)  # con CTkToplevel hay que esperar a que la ventana sea visible
        self.focus()

    def crear_label(self, texto, es_titulo=False):
        if es_titulo:
            ctk.CTkLabel(
                self, text=texto, text_color=MARRON_OSCURO, font=("Arial", 20, "bold")
            ).pack(pady=(20, 15))
        else:
            ctk.CTkLabel(
                self, text=texto, text_color=MARRON, font=("Arial", 13, "bold")
            ).pack(anchor="w", padx=40)

    def crear_entrada(self):
        entry = ctk.CTkEntry(
            self, height=38, corner_radius=RADIO, fg_color="white", text_color="black",
            border_width=0, font=("Arial", 14)
        )
        entry.pack(fill=tk.X, padx=40, pady=(2, 10))
        return entry

    def crear_combo(self, opciones):
        combo = crear_combo(self, opciones)
        combo.pack(fill=tk.X, padx=40, pady=(2, 10))
        return combo

    def crear_boton(self, texto, comando):
        ctk.CTkButton(
            self, text=texto, command=comando, height=38, corner_radius=RADIO,
            fg_color=MARRON, hover_color=MARRON_OSCURO, text_color="white",
            font=("Arial", 14, "bold")
        ).pack(fill=tk.X, padx=40, pady=(15, 20))


class VentanaNuevaVenta(FormularioBase):
    """Ventana modal interactiva para realizar una venta (Carrito de compras)."""
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Procesar Nueva Venta", "720x640")
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

        # Selección de Cliente
        frame_cliente = ctk.CTkFrame(self, fg_color="transparent")
        frame_cliente.pack(fill=tk.X, padx=20, pady=5)

        ctk.CTkLabel(frame_cliente, text="Cliente:", text_color=MARRON,
                     font=("Arial", 13, "bold")).pack(side=tk.LEFT)
        self.opciones_cli = [f"{c[0]} - {c[1]} {c[2]}" for c in self.lista_clientes_cache]
        self.combo_cliente = crear_combo(frame_cliente, self.opciones_cli)
        self.combo_cliente.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Selección de Producto y Cantidad
        frame_prod = ctk.CTkFrame(self, fg_color=BG_MENU, corner_radius=RADIO)
        frame_prod.pack(fill=tk.X, padx=20, pady=10)

        ctk.CTkLabel(frame_prod, text="Producto:", text_color=MARRON_OSCURO,
                     font=("Arial", 13, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))
        self.opciones_prod = [f"{p[0]} - {p[1]} (Stock: {p[3]})" for p in self.lista_productos_cache]
        self.combo_producto = crear_combo(frame_prod, self.opciones_prod, width=330)
        self.combo_producto.grid(row=1, column=0, padx=15, pady=(2, 12))

        ctk.CTkLabel(frame_prod, text="Cantidad:", text_color=MARRON_OSCURO,
                     font=("Arial", 13, "bold")).grid(row=0, column=1, sticky="w", padx=5, pady=(10, 0))
        self.entry_cantidad = ctk.CTkEntry(
            frame_prod, width=80, height=38, corner_radius=RADIO, fg_color="white",
            text_color="black", border_width=0, font=("Arial", 14), justify="center"
        )
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=1, column=1, padx=5, pady=(2, 12))

        ctk.CTkButton(
            frame_prod, text="➕ Agregar Item", command=self._agregar_al_carrito,
            width=150, height=38, corner_radius=RADIO, fg_color=MARRON,
            hover_color=MARRON_OSCURO, text_color="white", font=("Arial", 13, "bold")
        ).grid(row=1, column=2, padx=15, pady=(2, 12))

        # Tabla del Carrito
        self.tabla_cart = TablaTarjeta(self, self)
        self.tabla_cart.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.tabla_cart.configurar_columnas([
            ("prod", "Producto", 260, tk.W),
            ("precio", "P. Unit", 100, tk.E),
            ("cant", "Cant.", 80, tk.CENTER),
            ("subtotal", "Subtotal", 110, tk.E),
        ])

        # Pie con Total y Botón de Procesar
        frame_pie = ctk.CTkFrame(self, fg_color="transparent")
        frame_pie.pack(fill=tk.X, padx=20, pady=(10, 20))

        self.lbl_total = ctk.CTkLabel(frame_pie, text="Total: $0.00", text_color=MARRON_OSCURO,
                                      font=("Arial", 20, "bold"))
        self.lbl_total.pack(side=tk.LEFT)

        ctk.CTkButton(
            frame_pie, text="✔ Finalizar Venta", command=self.guardar_venta,
            width=190, height=40, corner_radius=RADIO, fg_color=MARRON,
            hover_color=MARRON_OSCURO, text_color="white", font=("Arial", 14, "bold")
        ).pack(side=tk.RIGHT)

    def _agregar_al_carrito(self):
        idx_prod = indice_combo(self.combo_producto, self.opciones_prod)
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
        self.tabla_cart.limpiar()

        total = 0.0
        for item in self.carrito:
            total += item["subtotal"]
            self.tabla_cart.insertar((item["nombre"], f"${item['precio']:.2f}", item["cantidad"], f"${item['subtotal']:.2f}"))

        self.lbl_total.configure(text=f"Total: ${total:.2f}")

    def guardar_venta(self):
        idx_cli = indice_combo(self.combo_cliente, self.opciones_cli)
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
        super().__init__(parent, "Registrar Nuevo Producto", "380x520")
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

        # Seleccionar Proveedor mediante lista desplegable
        self.crear_label("Proveedor:")
        self.opciones_prov = [f"{p[0]} - {p[1]}" for p in self.lista_proveedores_cache]
        self.combo_prov = self.crear_combo(self.opciones_prov)

        # Resto de campos
        self.crear_label("Nombre del Producto:")
        self.entry_nombre = self.crear_entrada()
        self.crear_label("Categoría:")
        self.entry_categoria = self.crear_entrada()
        self.crear_label("Precio Actual:")
        self.entry_precio = self.crear_entrada()
        self.crear_label("Stock Inicial:")
        self.entry_stock = self.crear_entrada()

        self.crear_boton("Guardar Producto", self.guardar)

    def guardar(self):
        idx_prov = indice_combo(self.combo_prov, self.opciones_prov)
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
        super().__init__(parent, "Registrar Nuevo Proveedor", "380x450")
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

        self.crear_boton("Guardar Proveedor", self.guardar)

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
        super().__init__(parent, "Registrar Nuevo Cliente", "380x520")
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

        self.crear_boton("Guardar Cliente", self.guardar)

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
        self.root.geometry("1100x600")
        self.root.configure(fg_color=BG)

        configurar_estilos()
        self.botones_menu = {}
        self._crear_interfaz()
        self.cambiar_modulo("Productos")

    def _crear_interfaz(self):
        # Panel Lateral (Menú)
        frame_menu = ctk.CTkFrame(self.root, width=220, corner_radius=0, fg_color=BG_MENU)
        frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        frame_menu.pack_propagate(False)

        self.imagen_logo = cargar_logo()
        if self.imagen_logo:
            ctk.CTkLabel(frame_menu, image=self.imagen_logo, text="").pack(pady=(25, 20))
        else:
            ctk.CTkLabel(frame_menu, text="PANADERÍA COZI", text_color=MARRON_OSCURO,
                         font=("Arial", 16, "bold")).pack(pady=25)

        modulos = [
            ("📦 Productos", "Productos"),
            ("🛒 Ventas", "Ventas"),
            ("👥 Clientes", "Clientes"),
            ("🚚 Proveedores", "Proveedores")
        ]

        for texto, nombre in modulos:
            boton = ctk.CTkButton(
                frame_menu, text=texto, command=lambda m=nombre: self.cambiar_modulo(m),
                height=38, corner_radius=RADIO, fg_color=MARRON, hover_color=MARRON_HOVER,
                text_color="white", font=("Arial", 14, "bold"), anchor="w"
            )
            boton.pack(fill=tk.X, padx=15, pady=5)
            self.botones_menu[nombre] = boton

        # Panel Principal
        frame_trabajo = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_trabajo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Encabezado
        frame_superior = ctk.CTkFrame(frame_trabajo, fg_color="transparent")
        frame_superior.pack(fill=tk.X, padx=30, pady=20)

        self.label_titulo = ctk.CTkLabel(frame_superior, text="", text_color=MARRON_OSCURO,
                                         font=("Arial", 24, "bold"))
        self.label_titulo.pack(side=tk.LEFT)

        self.frame_acciones = ctk.CTkFrame(frame_superior, fg_color="transparent")
        self.frame_acciones.pack(side=tk.RIGHT)

        # Contenedor de Tabla
        self.tabla = TablaTarjeta(frame_trabajo, self.root)
        self.tabla.frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

    def _crear_boton_accion(self, texto, comando, color=MARRON, color_hover=MARRON_OSCURO):
        ctk.CTkButton(
            self.frame_acciones, text=texto, command=comando, height=36, corner_radius=RADIO,
            fg_color=color, hover_color=color_hover, text_color="white",
            font=("Arial", 13, "bold")
        ).pack(side=tk.LEFT, padx=5)

    def cambiar_modulo(self, nombre_modulo):
        self.label_titulo.configure(text=f"Módulo de {nombre_modulo}")

        # Resaltar el módulo activo en el menú
        for nombre, boton in self.botones_menu.items():
            boton.configure(fg_color=MARRON_OSCURO if nombre == nombre_modulo else MARRON)

        for widget in self.frame_acciones.winfo_children():
            widget.destroy()
        self.tabla.limpiar()

        if nombre_modulo == "Productos":
            self._cargar_modulo_productos()
        elif nombre_modulo == "Ventas":
            self._cargar_modulo_ventas()
        elif nombre_modulo == "Clientes":
            self._cargar_modulo_clientes()
        elif nombre_modulo == "Proveedores":
            self._cargar_modulo_proveedores()

    # ---------- Productos ----------
    def _cargar_modulo_productos(self):
        self._crear_boton_accion("+ Nuevo Producto",
                                 lambda: VentanaProducto(self.root, self.cambiar_modulo))
        self._crear_boton_accion("🗑 Eliminar Producto", self._eliminar_producto, ROJO, ROJO_HOVER)

        self.tabla.configurar_columnas([
            ("codigo", "Código", 80, tk.CENTER),
            ("nombre", "Producto", 250, tk.W),
            ("categoria", "Categoría", 150, tk.W),
            ("stock", "Stock", 90, tk.CENTER),
            ("precio", "Precio", 110, tk.E),
        ])

        for prod in ProductoDAO.obtener_todos():
            self.tabla.insertar(prod)

    def _eliminar_producto(self):
        """Elimina el producto seleccionado en la tabla previa confirmación."""
        valores = self.tabla.valores_seleccionados()

        if not valores:
            messagebox.showwarning("Atención", "Por favor, seleccione un producto de la tabla para eliminar.")
            return

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

    # ---------- Ventas ----------
    def _cargar_modulo_ventas(self):
        self._crear_boton_accion("+ Procesar Venta",
                                 lambda: VentanaNuevaVenta(self.root, self.cambiar_modulo))

        self.tabla.configurar_columnas([
            ("id_venta", "Nº Venta", 90, tk.CENTER),
            ("cliente", "Cliente", 250, tk.W),
            ("fecha", "Fecha / Hora", 180, tk.CENTER),
            ("total", "Total ($)", 120, tk.E),
        ])

        try:
            ventas = VentaDAO.obtener_historial()
            for v in ventas:
                self.tabla.insertar((v[0], v[1], v[2], f"${float(v[3]):.2f}"))
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las ventas: {e}")

    # ---------- Clientes ----------
    def _cargar_modulo_clientes(self):
        self._crear_boton_accion("+ Nuevo Cliente",
                                 lambda: VentanaCliente(self.root, self.cambiar_modulo))
        self._crear_boton_accion("🗑 Eliminar Cliente", self._eliminar_cliente, ROJO, ROJO_HOVER)

        self.tabla.configurar_columnas([
            ("id", "ID", 50, tk.CENTER),
            ("nombre", "Nombre", 120, tk.W),
            ("apellido", "Apellido", 120, tk.W),
            ("email", "Correo Electrónico", 180, tk.W),
            ("telefono", "Teléfono", 100, tk.CENTER),
            ("direccion", "Dirección", 180, tk.W),
        ])

        for cli in ClienteDAO.obtener_todos():
            self.tabla.insertar(cli)

    def _eliminar_cliente(self):
        """Elimina el cliente seleccionado en la tabla previa confirmación."""
        valores = self.tabla.valores_seleccionados()

        if not valores:
            messagebox.showwarning("Atención", "Por favor, seleccione un cliente de la tabla para eliminar.")
            return

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

    # ---------- Proveedores ----------
    def _cargar_modulo_proveedores(self):
        self._crear_boton_accion("+ Nuevo Proveedor",
                                 lambda: VentanaProveedor(self.root, self.cambiar_modulo))
        self._crear_boton_accion("🗑 Eliminar Proveedor", self._eliminar_proveedor, ROJO, ROJO_HOVER)

        self.tabla.configurar_columnas([
            ("id", "Código", 70, tk.CENTER),
            ("empresa", "Empresa", 200, tk.W),
            ("contacto", "Contacto", 150, tk.W),
            ("telefono", "Teléfono", 120, tk.CENTER),
            ("email", "Correo Electrónico", 200, tk.W),
        ])

        for prov in ProveedorDAO.obtener_todos():
            self.tabla.insertar(prov)

    def _eliminar_proveedor(self):
        """Elimina el proveedor seleccionado en la tabla previa confirmación."""
        valores = self.tabla.valores_seleccionados()

        if not valores:
            messagebox.showwarning("Atención", "Por favor, seleccione un proveedor de la tabla para eliminar.")
            return

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
    root = ctk.CTk()
    app = SistemaPanaderia(root)
    root.mainloop()