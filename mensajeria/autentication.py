from bd import conectar_bd
from tkinter import messagebox
import pyodbc

def registrar_usuario(nombre, apellido, correo, telefono, contrasena):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_RegistrarUsuario ?, ?, ?, ?, ?", 
                       (nombre, apellido, contrasena, correo, telefono))
        conn.commit()
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
    except pyodbc.IntegrityError:
        messagebox.showerror("Error", "El correo o teléfono ya está registrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    finally:
        conn.close()

def iniciar_sesion(correo, contrasena):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_LoginUsuario ?, ?", correo, contrasena)
        resultado = cursor.fetchone()
        if resultado:
            columnas = [col[0] for col in cursor.description]
            return dict(zip(columnas, resultado))
        return None
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def cerrar_sesion(usuario_id):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_CerrarSesion @param_UsuarioID = ?", usuario_id)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cerrar la sesión:\n{e}")
    finally:
        conn.close()