import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def verificar_acceso():
    usuario = entrada_usuario.get()
    password = entrada_pass.get()
    
    if usuario == "Panaderia" and password == "1234":
        ventana_login.destroy()
        script_interfaz = os.path.join(os.path.dirname(__file__), "interfaz.py")
        subprocess.run([sys.executable, script_interfaz])
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos. Intente nuevamente.")
        entrada_pass.delete(0, tk.END)
        entrada_usuario.focus()

ventana_login = tk.Tk()
ventana_login.title("Acceso al Sistema - Panadería Cozi")
ventana_login.geometry("380x300")
ventana_login.configure(bg="#2c3e50")
ventana_login.resizable(False, False)

tk.Label(ventana_login, text="Panadería Cozi", bg="#2c3e50", fg="#1abc9c", font=("Arial", 18, "bold")).pack(pady=(20, 10))
tk.Label(ventana_login, text="Acceso al Sistema", bg="#2c3e50", fg="white", font=("Arial", 11)).pack(pady=(0, 15))

tk.Label(ventana_login, text="Usuario", bg="#2c3e50", fg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=45)
entrada_usuario = tk.Entry(ventana_login, font=("Arial", 12), bd=0)
entrada_usuario.pack(pady=(2, 10), ipadx=5, ipady=3, fill=tk.X, padx=45)
entrada_usuario.focus()

tk.Label(ventana_login, text="Contraseña", bg="#2c3e50", fg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=45)
entrada_pass = tk.Entry(ventana_login, show="*", font=("Arial", 12), bd=0)
entrada_pass.pack(pady=(2, 15), ipadx=5, ipady=3, fill=tk.X, padx=45)

tk.Button(ventana_login, text="Ingresar", command=verificar_acceso, font=("Arial", 10, "bold"), bg="#1abc9c", fg="white", bd=0, height=2, cursor="hand2").pack(fill=tk.X, padx=45)

ventana_login.mainloop()