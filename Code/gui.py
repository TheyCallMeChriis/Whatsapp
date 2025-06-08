import tkinter as tk
from tkinter import messagebox
import pyodbc

# Conexión SQL Server
def conectar_bd():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=MensajeriaBD;"
        "Trusted_Connection=yes;"
    )

# Centrado de ventanas
def centrar_ventana(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# Registro de usuario
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

        # Ejecutar procedimiento de registro
        cursor.execute("""
            EXEC sp_RegistrarUsuario ?, ?, ?, ?, ?
        """, (nombre, apellido, contrasena, correo, telefono))

        conn.commit()
        conn.close()
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
    except pyodbc.IntegrityError:
        messagebox.showerror("Error", "El correo o número de teléfono ya está registrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Iniciar sesión
def iniciar_sesion():
    identificador = entry_login_correo.get()
    contrasena = entry_login_pass.get()

    if not (identificador and contrasena):
        messagebox.showwarning("Campos vacíos", "Debe ingresar todos los datos.")
        return

    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para login
        cursor.execute("""
            EXEC sp_LoginUsuario ?, ?
        """, (identificador, contrasena))

        resultado = cursor.fetchone()

        if resultado:
            usuario_id = resultado.UsuarioID
            token = resultado.Token
            messagebox.showinfo("Login exitoso", f"ID de usuario: {usuario_id}\nToken de sesión: {token}")
        else:
            messagebox.showerror("Login fallido", "Credenciales incorrectas o usuario inactivo.")

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        print(f"Error: {e}")

# Ventana de login
def mostrar_login():
    global entry_login_correo, entry_login_pass  # Definir las variables globalmente
    login_win = tk.Toplevel(ventana)
    login_win.title("Login")
    login_win.geometry("350x330")
    login_win.configure(bg="#EAF0FA")
    centrar_ventana(login_win)

    frame = tk.Frame(login_win, bg="white", padx=20, pady=20)
    frame.pack(pady=30, padx=30)

    tk.Label(frame, text="Login", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

    tk.Label(frame, text="📧 Correo Electrónico", font=("Segoe UI", 10), bg="white").pack(anchor="w")
    entry_login_correo = tk.Entry(frame, width=35)
    entry_login_correo.pack(pady=(0, 10))

    tk.Label(frame, text="🔒 Contraseña", font=("Segoe UI", 10), bg="white").pack(anchor="w")
    entry_login_pass = tk.Entry(frame, show="*", width=35)
    entry_login_pass.pack(pady=(0, 10))

    tk.Button(frame, text="Login", bg="#0D1A2B", fg="white", width=30,
              font=("Segoe UI", 10, "bold"), command=iniciar_sesion).pack(pady=10)

    tk.Label(frame, text="¿No tienes cuenta? Regístrate", font=("Segoe UI", 9), bg="white").pack()

# INTERFAZ PRINCIPAL
ventana = tk.Tk()
ventana.title("Registro")
ventana.geometry("450x530")
ventana.configure(bg="#DDEAFE")
centrar_ventana(ventana)

frame = tk.Frame(ventana, bg="white", padx=20, pady=20)
frame.pack(pady=30)

tk.Label(frame, text="Regístrate", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

# Campos
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

# Botón registrar
tk.Button(frame, text="Registrarte", bg="#0D1A2B", fg="white", width=30,
          font=("Segoe UI", 10, "bold"), command=registrar_usuario).pack(pady=10)

tk.Label(frame, text="Al registrarte, aceptas nuestras Condiciones de uso y Política de privacidad.",
         font=("Segoe UI", 8), bg="white", wraplength=300, justify="center").pack(pady=5)

tk.Button(frame, text="¿Ya tienes una cuenta? Iniciar Sesión", bg="white", fg="#0D6EFD", bd=0,
          font=("Segoe UI", 9, "bold"), command=mostrar_login).pack()

ventana.mainloop()
