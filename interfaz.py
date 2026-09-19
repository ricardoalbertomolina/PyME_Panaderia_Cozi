#Es el front de la pagina de la panaderia.

import tkinter as tk
from tkinter import ttk
from acceso_a_datos import obtener_productos

def cargar_datos_productos():
    """Limpia la tabla y carga los datos desde la base de datos."""
    for fila in tabla_productos.get_children():
        tabla_productos.delete(fila)
    
    # Obtener datos de acceso_a_datos.py
    productos = obtener_productos()
    
    # Insertar filas en la tabla
    for producto in productos:
        tabla_productos.insert("", tk.END, values=producto)

def mostrar_mensaje(modulo):
    print(f"Ingresando al módulo: {modulo}")

# 1. Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema de Ventas - Panadería Cozy")
root.geometry("900x500")

# 2. Panel Izquierdo (Menú)
frame_menu = tk.Frame(root, bg="#2c3e50", width=200)
frame_menu.pack(side=tk.LEFT, fill=tk.Y)

# Botones del menú
tk.Label(frame_menu, text="MENÚ", bg="#2c3e50", fg="white", font=("Arial", 14, "bold")).pack(pady=20)
tk.Button(frame_menu, text="Productos", width=20, command=cargar_datos_productos).pack(pady=10)
tk.Button(frame_menu, text="Ventas", width=20, command=lambda: mostrar_mensaje("Ventas")).pack(pady=10)
tk.Button(frame_menu, text="Clientes", width=20, command=lambda: mostrar_mensaje("Clientes")).pack(pady=10)
tk.Button(frame_menu, text="Proveedores", width=20, command=lambda: mostrar_mensaje("Proveedores")).pack(pady=10)

# 3. Panel Derecho (Área de trabajo)
frame_trabajo = tk.Frame(root, bg="#ecf0f1")
frame_trabajo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(frame_trabajo, text="Módulo de Productos", bg="#ecf0f1", font=("Arial", 16, "bold")).pack(pady=10)

# 4. Configurar la Tabla (Treeview)
columnas = ("codigo", "nombre", "categoria", "stock", "precio")
tabla_productos = ttk.Treeview(frame_trabajo, columns=columnas, show="headings")

# Definir encabezados
tabla_productos.heading("codigo", text="Código")
tabla_productos.heading("nombre", text="Producto")
tabla_productos.heading("categoria", text="Categoría")
tabla_productos.heading("stock", text="Stock")
tabla_productos.heading("precio", text="Precio")

# Ajustar columnas
tabla_productos.column("codigo", width=50, anchor=tk.CENTER)
tabla_productos.column("nombre", width=200)
tabla_productos.column("categoria", width=120)
tabla_productos.column("stock", width=80, anchor=tk.CENTER)
tabla_productos.column("precio", width=100, anchor=tk.E)

tabla_productos.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Cargar los datos al iniciar la aplicación
cargar_datos_productos()

# Iniciar el bucle de la aplicación
root.mainloop()