#Es el front de la pagina de la panaderia.
import tkinter as tk
from tkinter import ttk
from acceso_a_datos import obtener_productos, obtener_clientes

def cambiar_modulo(nombre_modulo):
    label_titulo.config(text=f"Módulo de {nombre_modulo}")
    
    for fila in tabla_datos.get_children():
        tabla_datos.delete(fila)
        
    if nombre_modulo == "Productos":
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

label_titulo = tk.Label(frame_trabajo, text="Módulo de Productos", bg="#f4f6f7", fg="#2c3e50", font=("Arial", 18, "bold"))
label_titulo.pack(pady=25, anchor="w", padx=30)

frame_tabla = tk.Frame(frame_trabajo, bg="white", bd=1, relief=tk.SOLID)
frame_tabla.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

tabla_datos = ttk.Treeview(frame_tabla, show="headings")
tabla_datos.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla_datos.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tabla_datos.configure(yscrollcommand=scrollbar.set)

cambiar_modulo("Productos")

root.mainloop()