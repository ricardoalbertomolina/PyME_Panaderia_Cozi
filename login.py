import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def verificar_acceso():
    password = entrada_pass.get()
    if password == "1234":
        ventana_login.destroy()
        script_interfaz = os.path.join(os.path.dirname(__file__), "interfaz.py")
        subprocess.run([sys.executable, script_interfaz])
    else:
        messagebox.showerror("Error", "Contraseña incorrecta. Intente nuevamente.")
        entrada_pass.delete(0, tk.END)

ventana_login = tk.Tk()
ventana_login.title("Acceso al Sistema")
ventana_login.geometry("350x220")
ventana_login.configure(bg="#2c3e50")
ventana_login.resizable(False, False)

tk.Label(ventana_login, text="Ingrese la Contraseña", bg="#2c3e50", fg="white", font=("Arial", 14, "bold")).pack(pady=25)

entrada_pass = tk.Entry(ventana_login, show="*", font=("Arial", 14), justify="center", bd=0)
entrada_pass.pack(pady=5, ipadx=10, ipady=5)
entrada_pass.focus()

tk.Button(ventana_login, text="Ingresar", command=verificar_acceso, font=("Arial", 10, "bold"), bg="white", fg="#2c3e50", bd=0, width=12, height=2, cursor="hand2").pack(pady=20)

ventana_login.mainloop()