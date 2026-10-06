import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw
import subprocess
import sys
import os

# ---------- Paleta ----------
BG = "#eedeb8"
GRIS_ICONO = "#7f8c8d"
COLOR_BOTON = "#ac6d3c"
COLOR_BOTON_HOVER = "#763e12"

CARPETA = os.path.dirname(os.path.abspath(__file__))   # carpeta Interfaz
RAIZ_PROYECTO = os.path.dirname(CARPETA)               # carpeta del proyecto

# Logo: PNG sin fondo dentro de la carpeta "img" (Interfaz/img/logo.png)
RUTA_LOGO = os.path.join(CARPETA, "img", "logo.png")
TAMANO_LOGO = (250, 100)  # (ancho máximo, alto máximo)

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


def crear_icono_ojo(tachado):
    """Dibuja el ícono del ojo (con o sin tachado) como CTkImage."""
    t = 96  # se dibuja grande y se reduce para que quede suave
    img = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((6, 24, 90, 72), outline=GRIS_ICONO, width=8)
    d.ellipse((36, 36, 60, 60), fill=GRIS_ICONO)
    if tachado:
        d.line((14, 84, 82, 12), fill=GRIS_ICONO, width=8)
    return ctk.CTkImage(light_image=img, dark_image=img, size=(22, 22))


def iniciar_login():
    password_oculta = True

    def alternar_password():
        nonlocal password_oculta
        password_oculta = not password_oculta
        entrada_pass.configure(show="*" if password_oculta else "")
        boton_ojo.configure(image=icono_tachado if password_oculta else icono_ojo)

    def verificar_acceso():
        usuario = entrada_usuario.get()
        password = entrada_pass.get()

        if usuario == "panaderia" and password == "1234":
            ventana_login.destroy()
            script_interfaz = os.path.join(CARPETA, "interfaz.py")
            # Se agrega la raíz del proyecto al path para que interfaz.py
            # pueda importar las carpetas Datos y Conexion
            entorno = os.environ.copy()
            entorno["PYTHONPATH"] = RAIZ_PROYECTO + os.pathsep + entorno.get("PYTHONPATH", "")
            subprocess.run([sys.executable, script_interfaz], env=entorno, cwd=RAIZ_PROYECTO)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos. Intente nuevamente.")
            entrada_pass.delete(0, "end")
            entrada_usuario.focus()

    def olvide_password(event=None):
        messagebox.showinfo("Recuperar contraseña",
                            "Contactá al administrador del sistema para restablecer tu contraseña.")

    ventana_login = ctk.CTk()
    ventana_login.title("Acceso al Sistema - Panadería Cozi")
    ventana_login.geometry("380x430")
    ventana_login.configure(fg_color=BG)
    ventana_login.resizable(False, False)

    # Logo (si no se encuentra, se muestra el texto como respaldo)
    imagen_logo = cargar_logo()
    if imagen_logo:
        ctk.CTkLabel(ventana_login, image=imagen_logo, text="").pack(pady=(15, 5))
    else:
        ctk.CTkLabel(ventana_login, text="Panadería Cozi", text_color=COLOR_BOTON,
                     font=("Arial", 22, "bold")).pack(pady=(20, 10))

    ctk.CTkLabel(ventana_login, text="Acceso al Sistema", text_color="#3e3e3e",
                 font=("Arial", 14)).pack(pady=(0, 15))

    # Usuario
    ctk.CTkLabel(ventana_login, text="Usuario", text_color="#ac6d3c",
                 font=("Arial", 13, "bold")).pack(anchor="w", padx=45)
    entrada_usuario = ctk.CTkEntry(ventana_login, width=290, height=38, corner_radius=14,
                                   fg_color="white", text_color="black", border_width=0,
                                   font=("Arial", 14))
    entrada_usuario.pack(pady=(2, 10), padx=45)
    entrada_usuario.focus()

    # Contraseña (con ojito)
    ctk.CTkLabel(ventana_login, text="Contraseña", text_color="#ac6d3c",
                 font=("Arial", 13, "bold")).pack(anchor="w", padx=45)
    entrada_pass = ctk.CTkEntry(ventana_login, width=290, height=38, corner_radius=14,
                                fg_color="white", text_color="black", border_width=0,
                                font=("Arial", 14), show="*")
    entrada_pass.pack(pady=(2, 4), padx=45)

    icono_ojo = crear_icono_ojo(tachado=False)
    icono_tachado = crear_icono_ojo(tachado=True)

    boton_ojo = ctk.CTkButton(ventana_login, text="", image=icono_tachado, width=30, height=28,
                              fg_color="white", hover_color="white", bg_color="white",
                              corner_radius=0, cursor="hand2", command=alternar_password)
    boton_ojo.place(in_=entrada_pass, relx=1.0, x=-10, rely=0.5, anchor="e")

    # ¿Olvidaste tu contraseña?
    lbl_olvide = ctk.CTkLabel(ventana_login, text="¿Olvidaste tu contraseña?",
                              text_color="#e74c3c", font=("Arial", 12), cursor="hand2")
    lbl_olvide.pack(anchor="e", padx=45)
    lbl_olvide.bind("<Button-1>", olvide_password)

    # Botón de ingreso, separado de los inputs
    ctk.CTkButton(ventana_login, text="Ingresar", command=verificar_acceso,
                  width=290, height=38, corner_radius=14, fg_color=COLOR_BOTON,
                  hover_color=COLOR_BOTON_HOVER, text_color="white",
                  font=("Arial", 14, "bold")).pack(padx=45, pady=(40, 20))

    # Enter también confirma el ingreso (teclado principal y teclado numérico)
    ventana_login.bind("<Return>", lambda event: verificar_acceso())
    ventana_login.bind("<KP_Enter>", lambda event: verificar_acceso())

    ventana_login.mainloop()


# Para permitir ejecutarlo tanto desde main.py como de forma directa
if __name__ == "__main__":
    iniciar_login()