import pyodbc
import tkinter as tk
from tkinter import messagebox

# Función para conectar a la base de datos
def conectar_bd():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=MensajeriaBD;"
        "Trusted_Connection=yes;"
    )


# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre = entry_register_nombre.get()
    apellido = entry_register_apellido.get()
    correo = entry_register_correo.get()
    telefono = entry_register_telefono.get()
    contrasena = entry_register_pass.get()

    if not (nombre and apellido and correo and telefono and contrasena):
        messagebox.showwarning("Campos vacíos", "Debe ingresar todos los datos.")
        return

    try:
        conn = conectar_bd()
        if conn is None:
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
            return

        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para registrar un nuevo usuario
        cursor.execute("""
            EXEC sp_RegistrarUsuario ?, ?, ?, ?, ?
        """, (nombre, apellido, contrasena, correo, telefono))

        conn.commit()  # Confirmar la transacción
        conn.close()

        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")

    except pyodbc.Error as e:
        messagebox.showerror("Error en la base de datos", f"Error al registrar usuario: {e}")
        print(f"Error en la base de datos: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        print(f"Error: {e}")

# Función para iniciar sesión
def iniciar_sesion():
    identificador = entry_login_correo.get()  # Obtener correo o número de teléfono
    contrasena = entry_login_pass.get()  # Obtener contraseña

    if not (identificador and contrasena):  # Validar que ambos campos tengan datos
        messagebox.showwarning("Campos vacíos", "Debe ingresar todos los datos.")
        return

    try:
        conn = conectar_bd()  # Conectar a la base de datos
        if conn is None:
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
            return

        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para login
        cursor.execute("""
            EXEC sp_LoginUsuario ?, ?
        """, (identificador, contrasena))

        # Obtener el resultado
        resultado = cursor.fetchone()

        if resultado:  # Si se obtiene un resultado, el login fue exitoso
            usuario_id = resultado.UsuarioID
            token = resultado.Token
            messagebox.showinfo("Login exitoso", f"ID de usuario: {usuario_id}\nToken de sesión: {token}")
        else:  # Si no se obtiene un resultado, hubo un error en las credenciales
            messagebox.showerror("Login fallido", "Credenciales incorrectas o usuario inactivo.")

        conn.close()  # Cerrar la conexión a la base de datos

    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")
        print(f"Error en la base de datos: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        print(f"Error: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Mensajería")

# **Interfaz de Registro**
frame_register = tk.Frame(root)
frame_register.pack(pady=10)

# Labels y entradas para el registro
tk.Label(frame_register, text="Nombre:").grid(row=0, column=0)
entry_register_nombre = tk.Entry(frame_register)
entry_register_nombre.grid(row=0, column=1)

tk.Label(frame_register, text="Apellido:").grid(row=1, column=0)
entry_register_apellido = tk.Entry(frame_register)
entry_register_apellido.grid(row=1, column=1)

tk.Label(frame_register, text="Correo:").grid(row=2, column=0)
entry_register_correo = tk.Entry(frame_register)
entry_register_correo.grid(row=2, column=1)

tk.Label(frame_register, text="Teléfono:").grid(row=3, column=0)
entry_register_telefono = tk.Entry(frame_register)
entry_register_telefono.grid(row=3, column=1)

tk.Label(frame_register, text="Contraseña:").grid(row=4, column=0)
entry_register_pass = tk.Entry(frame_register, show="*")
entry_register_pass.grid(row=4, column=1)

tk.Button(frame_register, text="Registrar", command=registrar_usuario).grid(row=5, columnspan=2, pady=5)

# **Interfaz de Login**
frame_login = tk.Frame(root)
frame_login.pack(pady=10)

# Labels y entradas para el login
tk.Label(frame_login, text="Correo o Teléfono:").grid(row=0, column=0)
entry_login_correo = tk.Entry(frame_login)
entry_login_correo.grid(row=0, column=1)

tk.Label(frame_login, text="Contraseña:").grid(row=1, column=0)
entry_login_pass = tk.Entry(frame_login, show="*")
entry_login_pass.grid(row=1, column=1)

tk.Button(frame_login, text="Iniciar sesión", command=iniciar_sesion).grid(row=2, columnspan=2, pady=5)

# Ejecutar la aplicación
root.mainloop()
