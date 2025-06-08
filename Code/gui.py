import tkinter as tk
from tkinter import messagebox
import pyodbc

# ---------------------------- CONEXIÓN A BASE DE DATOS ----------------------------

def conectar_bd():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=MensajeriaBD;"
        "Trusted_Connection=yes;"
    )

# ---------------------------- CENTRAR VENTANA ----------------------------

def centrar_ventana(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ---------------------------- REGISTRAR USUARIO ----------------------------

def registrar_usuario():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    correo = entry_correo.get()
    telefono = entry_telefono.get()
    contrasena = entry_password.get()

    if not (nombre and apellido and correo and telefono and contrasena):
        messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
        return

    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("EXEC sp_RegistrarUsuario ?, ?, ?, ?, ?", 
                    (nombre, apellido, contrasena, correo, telefono))
        conn.commit()
        conn.close()

        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
    except pyodbc.IntegrityError:
        messagebox.showerror("Error", "El correo o teléfono ya está registrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# ---------------------------- INICIAR SESIÓN ----------------------------

def iniciar_sesion():
    correo = entry_login_correo.get()
    contrasena = entry_login_pass.get()

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute("EXEC sp_LoginUsuario ?, ?", correo, contrasena)
        resultado = cursor.fetchone()

        if resultado:
            columnas = [col[0] for col in cursor.description]
            data = dict(zip(columnas, resultado))

            if data.get("UsuarioID") and data.get("Token"):
                usuario_id = data["UsuarioID"]
                token = data["Token"]
                messagebox.showinfo("Bienvenido", f"Bienvenido usuario {usuario_id}")
                mostrar_interfaz_principal(usuario_id, token)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        else:
            messagebox.showerror("Error", "No se recibió respuesta del servidor.")

        cursor.close()
        conexion.close()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# ---------------------------- VENTANA DE LOGIN ----------------------------

def mostrar_login():
    login_win = tk.Toplevel(ventana)
    login_win.title("Iniciar sesión")
    login_win.geometry("400x300")
    login_win.configure(bg="#EAF0FA")
    centrar_ventana(login_win)

    frame = tk.Frame(login_win, bg="white", padx=20, pady=20)
    frame.pack(pady=30)

    tk.Label(frame, text="Iniciar sesión", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

    tk.Label(frame, text="📧 Correo electrónico", font=("Segoe UI", 10), bg="white").pack(anchor="w")
    global entry_login_correo
    entry_login_correo = tk.Entry(frame, width=35)
    entry_login_correo.pack(pady=(0, 10))

    tk.Label(frame, text="🔒 Contraseña", font=("Segoe UI", 10), bg="white").pack(anchor="w")
    global entry_login_pass
    entry_login_pass = tk.Entry(frame, show="*", width=35)
    entry_login_pass.pack(pady=(0, 15))

    tk.Button(frame, text="Iniciar sesión", bg="#0D1A2B", fg="white", width=30,
            font=("Segoe UI", 10, "bold"), command=iniciar_sesion).pack(pady=10)

# ---------------------------- INTERFAZ PRINCIPAL TRAS LOGIN ----------------------------

def mostrar_interfaz_principal(usuario_id, token):
    ventana_chat = tk.Toplevel(ventana)
    ventana_chat.title("Mensajería")
    ventana_chat.geometry("800x600")
    ventana_chat.configure(bg="white")
    centrar_ventana(ventana_chat)

    label = tk.Label(ventana_chat, text=f"Bienvenido, usuario {usuario_id}", font=("Segoe UI", 14), bg="white")
    label.pack(pady=20)

# ---------------------------- INTERFAZ DE REGISTRO ----------------------------

ventana = tk.Tk()
ventana.title("Registro")
ventana.geometry("450x530")
ventana.configure(bg="#DDEAFE")
centrar_ventana(ventana)

frame = tk.Frame(ventana, bg="white", padx=20, pady=20)
frame.pack(pady=30)

tk.Label(frame, text="Regístrate", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

tk.Label(frame, text="👤 Nombre", font=("Segoe UI", 10), bg="white").pack(anchor="w")
entry_nombre = tk.Entry(frame, width=35)
entry_nombre.pack(pady=(0, 10))

tk.Label(frame, text="👥 Apellido", font=("Segoe UI", 10), bg="white").pack(anchor="w")
entry_apellido = tk.Entry(frame, width=35)
entry_apellido.pack(pady=(0, 10))

tk.Label(frame, text="📧 Correo", font=("Segoe UI", 10), bg="white").pack(anchor="w")
entry_correo = tk.Entry(frame, width=35)
entry_correo.pack(pady=(0, 10))

tk.Label(frame, text="📞 Teléfono", font=("Segoe UI", 10), bg="white").pack(anchor="w")
entry_telefono = tk.Entry(frame, width=35)
entry_telefono.pack(pady=(0, 10))

tk.Label(frame, text="🔒 Contraseña", font=("Segoe UI", 10), bg="white").pack(anchor="w")
entry_password = tk.Entry(frame, show="*", width=35)
entry_password.pack(pady=(0, 15))

tk.Button(frame, text="Registrarte", bg="#0D1A2B", fg="white", width=30,
        font=("Segoe UI", 10, "bold"), command=registrar_usuario).pack(pady=10)

tk.Label(frame, text="Al registrarte, aceptas nuestras Condiciones de uso y Política de privacidad.",
        font=("Segoe UI", 8), bg="white", wraplength=300, justify="center").pack(pady=5)

tk.Button(frame, text="¿Ya tienes una cuenta? Iniciar Sesión", bg="white", fg="#0D6EFD", bd=0,
        font=("Segoe UI", 9, "bold"), command=mostrar_login).pack()

ventana.mainloop()
