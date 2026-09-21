import tkinter as tk
from tkinter import ttk, messagebox
from Acceso_datos.acceso_a_datos import obtener_productos, obtener_clientes
from Conexion.conexion import conectar

def abrir_ventana_agregar_producto():
    def guardar_producto():
        nombre = entry_nombre.get().strip()
        categoria = entry_categoria.get().strip()
        precio = entry_precio.get().strip()
        stock = entry_stock.get().strip()
        id_prov = entry_prov.get().strip()
        
        if not nombre or not precio or not stock or not id_prov:
            messagebox.showerror("Error", "Por favor completa los campos obligatorios.")
            return
            
        try:
            p_val = float(precio)
            s_val = int(stock)
            prov_val = int(id_prov)
            
            conexion = conectar()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO producto (id_proveedor, nombre, categoria, precio_actual, stock) VALUES (?, ?, ?, ?, ?)",
                    (prov_val, nombre, categoria, p_val, s_val)
                )
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Producto guardado correctamente.")
                ven_agregar.destroy()
                cambiar_modulo("Productos")
        except ValueError:
            messagebox.showerror("Error", "Precio, Stock y ID Proveedor deben ser numéricos.")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar: {e}")

    ven_agregar = tk.Toplevel(root)
    ven_agregar.title("Registrar Nuevo Producto")
    ven_agregar.geometry("350x400")
    ven_agregar.configure(bg="#2c3e50")
    ven_agregar.resizable(False, False)
    ven_agregar.grab_set()

    tk.Label(ven_agregar, text="Nuevo Producto", bg="#2c3e50", fg="#1abc9c", font=("Arial", 14, "bold")).pack(pady=15)

    tk.Label(ven_agregar, text="ID Proveedor:", bg="#2c3e50", fg="white", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
    global entry_prov
    entry_prov = tk.Entry(ven_agregar, font=("Arial", 11), bd=0)
    entry_prov.pack(pady=2, fill=tk.X, padx=30)

    tk.Label(ven_agregar, text="Nombre del Producto:", bg="#2c3e50", fg="white", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
    global entry_nombre
    entry_nombre = tk.Entry(ven_agregar, font=("Arial", 11), bd=0)
    entry_nombre.pack(pady=2, fill=tk.X, padx=30)

    tk.Label(ven_agregar, text="Categoría:", bg="#2c3e50", fg="white", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
    global entry_categoria
    entry_categoria = tk.Entry(ven_agregar, font=("Arial", 11), bd=0)
    entry_categoria.pack(pady=2, fill=tk.X, padx=30)

    tk.Label(ven_agregar, text="Precio Actual:", bg="#2c3e50", fg="white", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
    global entry_precio
    entry_precio = tk.Entry(ven_agregar, font=("Arial", 11), bd=0)
    entry_precio.pack(pady=2, fill=tk.X, padx=30)

    tk.Label(ven_agregar, text="Stock Inicial:", bg="#2c3e50", fg="white", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
    global entry_stock
    entry_stock = tk.Entry(ven_agregar, font=("Arial", 11), bd=0)
    entry_stock.pack(pady=2, fill=tk.X, padx=30)

    tk.Button(ven_agregar, text="Guardar Producto", command=guardar_producto, font=("Arial", 10, "bold"), bg="#1abc9c", fg="white", bd=0, height=2, cursor="hand2").pack(fill=tk.X, padx=30, pady=20)

def cambiar_modulo(nombre_modulo):
    label_titulo.config(text=f"Módulo de {nombre_modulo}")
    
    for widget in frame_acciones.winfo_children():
        widget.destroy()
        
    for fila in tabla_datos.get_children():
        tabla_datos.delete(fila)
        
    if nombre_modulo == "Productos":
        btn_nuevo = tk.Button(frame_acciones, text="+ Nuevo Producto", command=abrir_ventana_agregar_producto, font=("Arial", 10, "bold"), bg="#27ae60", fg="white", bd=0, padx=10, pady=5, cursor="hand2")
        btn_nuevo.pack(side=tk.LEFT)
        
        tabla_datos["columns"] = ("codigo", "nombre", "categoria", "stock", "precio")
        tabla_datos.heading("codigo", text="Código")
        tabla_datos.heading("nombre", text="Producto")
        tabla_datos.heading("categoria", text="Categoría")
        tabla_datos.heading("stock", text="Stock")
        tabla_datos.heading("precio", text="Precio")
        
        tabla_datos.column("codigo", width=60, anchor=tk.CENTER)
        tabla_datos.column("nombre", width=220)
        tabla_datos.column("categoria", width=130)
        tabla_datos.column("stock", width=80, anchor=tk.CENTER)
        tabla_datos.column("precio", width=100, anchor=tk.E)
        
        productos = obtener_productos()
        for prod in productos:
            tabla_datos.insert("", tk.END, values=prod)
            
    elif nombre_modulo == "Clientes":
        tabla_datos["columns"] = ("nombre", "apellido", "email", "telefono", "direccion")
        tabla_datos.heading("nombre", text="Nombre")
        tabla_datos.heading("apellido", text="Apellido")
        tabla_datos.heading("email", text="Correo Electrónico")
        tabla_datos.heading("telefono", text="Teléfono")
        tabla_datos.heading("direccion", text="Dirección")
        
        tabla_datos.column("nombre", width=120)
        tabla_datos.column("apellido", width=120)
        tabla_datos.column("email", width=180)
        tabla_datos.column("telefono", width=100, anchor=tk.CENTER)
        tabla_datos.column("direccion", width=180)
        
        clientes = obtener_clientes()
        for cli in clientes:
            tabla_datos.insert("", tk.END, values=cli)
            
    else:
        tabla_datos["columns"] = ("mensaje",)
        tabla_datos.heading("mensaje", text="Información")
        tabla_datos.column("mensaje", width=500, anchor=tk.W)
        tabla_datos.insert("", tk.END, values=(f"Sección de {nombre_modulo} en desarrollo...",))

root = tk.Tk()
root.title("Sistema de Ventas - Panadería Cozy")
root.geometry("1050x550")
root.configure(bg="#f4f6f7")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#34495e", foreground="white")
style.configure("Treeview", font=("Arial", 10), rowheight=26)

frame_menu = tk.Frame(root, bg="#2c3e50", width=220)
frame_menu.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(frame_menu, text="PANADERÍA COZY", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12, "bold")).pack(pady=25)

btn_estilo = {"font": ("Arial", 10, "bold"), "bg": "#34495e", "fg": "white", "bd": 0, "activebackground": "#1abc9c", "activeforeground": "white", "height": 2}

tk.Button(frame_menu, text="📦 Productos", command=lambda: cambiar_modulo("Productos"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)
tk.Button(frame_menu, text="🛒 Ventas", command=lambda: cambiar_modulo("Ventas"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)
tk.Button(frame_menu, text="👥 Clientes", command=lambda: cambiar_modulo("Clientes"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)
tk.Button(frame_menu, text="🚚 Proveedores", command=lambda: cambiar_modulo("Proveedores"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)

frame_trabajo = tk.Frame(root, bg="#f4f6f7")
frame_trabajo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frame_superior_titulo = tk.Frame(frame_trabajo, bg="#f4f6f7")
frame_superior_titulo.pack(fill=tk.X, padx=30, pady=20)

label_titulo = tk.Label(frame_superior_titulo, text="Módulo de Productos", bg="#f4f6f7", fg="#2c3e50", font=("Arial", 18, "bold"))
label_titulo.pack(side=tk.LEFT)

frame_acciones = tk.Frame(frame_superior_titulo, bg="#f4f6f7")
frame_acciones.pack(side=tk.RIGHT)

frame_tabla = tk.Frame(frame_trabajo, bg="white", bd=1, relief=tk.SOLID)
frame_tabla.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

tabla_datos = ttk.Treeview(frame_tabla, show="headings")
tabla_datos.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla_datos.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tabla_datos.configure(yscrollcommand=scrollbar.set)

cambiar_modulo("Productos")

root.mainloop()