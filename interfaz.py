#Es el front de la pagina de la panaderia.

import tkinter as tk
from tkinter import ttk
from acceso_a_datos import obtener_productos

def cambiar_modulo(nombre_modulo):
    """Cambia el título superior y actualiza la pantalla según el botón presionado."""
    label_titulo.config(text=f"Módulo de {nombre_modulo}")
    
    # Limpiar la tabla actual al cambiar de sección
    for fila in tabla_datos.get_children():
        tabla_datos.delete(fila)
        
    if nombre_modulo == "Productos":
        # Configurar columnas para Productos
        tabla_datos["columns"] = ("codigo", "nombre", "categoria", "stock", "precio")
        tabla_datos.heading("codigo", text="Código")
        tabla_datos.heading("nombre", text="Producto")
        tabla_datos.heading("categoria", text="Categoría")
        tabla_datos.heading("stock", text="Stock")
        tabla_datos.heading("precio", text="Precio")
        
        # Cargar datos de productos
        productos = obtener_productos()
        for prod in productos:
            tabla_datos.insert("", tk.END, values=prod)
            
    else:
        # Configuración temporal para los demás módulos mientras los programamos
        tabla_datos["columns"] = ("mensaje",)
        tabla_datos.heading("mensaje", text=f"Información")
        tabla_datos.column("mensaje", width=500, anchor=tk.W)
        tabla_datos.insert("", tk.END, values=(f"Sección de {nombre_modulo} en desarrollo...",))

# 1. Ventana principal
root = tk.Tk()
root.title("Sistema de Ventas - Panadería Cozy")
root.geometry("1000x550")
root.configure(bg="#f4f6f7")

# Estilos modernos para los componentes
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#34495e", foreground="white")
style.configure("Treeview", font=("Arial", 10), rowheight=25)

# 2. Panel Izquierdo (Menú Lateral Estilizado)
frame_menu = tk.Frame(root, bg="#2c3e50", width=220)
frame_menu.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(frame_menu, text="PANADERÍA COZY", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12, "bold")).pack(pady=25)

# Botones del menú con diseño moderno
btn_estilo = {"font": ("Arial", 10, "bold"), "bg": "#34495e", "fg": "white", "bd": 0, "activebackground": "#1abc9c", "activeforeground": "white", "height": 2}

tk.Button(frame_menu, text="📦 Productos", command=lambda: cambiar_modulo("Productos"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)
tk.Button(frame_menu, text="🛒 Ventas", command=lambda: cambiar_modulo("Ventas"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)
tk.Button(frame_menu, text="👥 Clientes", command=lambda: cambiar_modulo("Clientes"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)
tk.Button(frame_menu, text="🚚 Proveedores", command=lambda: cambiar_modulo("Proveedores"), **btn_estilo).pack(fill=tk.X, padx=15, pady=5)

# 3. Panel Derecho (Área de Trabajo)
frame_trabajo = tk.Frame(root, bg="#f4f6f7")
frame_trabajo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Título dinámico superior
label_titulo = tk.Label(frame_trabajo, text="Módulo de Productos", bg="#f4f6f7", fg="#2c3e50", font=("Arial", 18, "bold"))
label_titulo.pack(pady=25, anchor="w", padx=30)

# 4. Contenedor de la Tabla
frame_tabla = tk.Frame(frame_trabajo, bg="white", bd=1, relief=tk.SOLID)
frame_tabla.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

tabla_datos = ttk.Treeview(frame_tabla, show="headings")
tabla_datos.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Scrollbar para la tabla
scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla_datos.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tabla_datos.configure(yscrollcommand=scrollbar.set)

# Cargar los datos iniciales de productos
cambiar_modulo("Productos")

root.mainloop()