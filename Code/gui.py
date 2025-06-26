import tkinter as tk
from tkinter import messagebox
import pyodbc

# ---------------------------- CONEXIÓN A BASE DE DATOS ----------------------------

usuario_id = None
token = None
ventana_chat = None

def conectar_bd():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=MensajeriaBD;"
        "Trusted_Connection=yes;",
        autocommit=True
    )

def obtener_mensajes(usuario_origen_id, usuario_destino_id):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerMensajes ?, ?", usuario_origen_id, usuario_destino_id)
        mensajes = cursor.fetchall()
        conn.close()
        return mensajes
    except Exception as e:
        print(f"Error al obtener mensajes: {e}")
        return []

def obtener_usuarios():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerUsuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

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
    global usuario_id, token
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
                mostrar_interfaz_principal()
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

def mostrar_interfaz_principal():
    global ventana_chat
    ventana_chat = tk.Toplevel(ventana)
    ventana_chat.title("Mensajería")
    ventana_chat.geometry("900x600")
    ventana_chat.configure(bg="white")
    centrar_ventana(ventana_chat)

    menubar = tk.Menu(ventana_chat)
    cuenta_menu = tk.Menu(menubar, tearoff=0)
    cuenta_menu.add_command(label="Cerrar sesión", command=cerrar_sesion)
    menubar.add_cascade(label="Inicio", menu=cuenta_menu)
    ventana_chat.config(menu=menubar)

    frame_principal = tk.Frame(ventana_chat, bg="gray", width=900, height=600)
    frame_principal.pack(fill="both", expand=True)

    panel_contactos = tk.Frame(frame_principal, bg="#F1F1F1", width=250)
    panel_contactos.pack(side="left", fill="y")

    tk.Label(panel_contactos, text="Contactos", font=("Segoe UI", 12, "bold"), bg="#F1F1F1").pack(pady=10)
    lista_contactos = tk.Listbox(panel_contactos, font=("Segoe UI", 10), width=30)
    lista_contactos.pack(padx=10, pady=5, fill="y", expand=True)

    usuarios = obtener_usuarios()
    contactos_dict = {}

    for idx, usuario in enumerate(usuarios):
        nombre_completo = f"{usuario.Nombre} {usuario.Apellido}"
        lista_contactos.insert(tk.END, nombre_completo)
        contactos_dict[idx] = (usuario.UsuarioID, nombre_completo)

    panel_chat = tk.Frame(frame_principal, bg="white")
    panel_chat.pack(side="right", fill="both", expand=True)

    tk.Label(panel_chat, text=f"Usuario ID: {usuario_id}", font=("Segoe UI", 10), bg="white", anchor="w").pack(fill="x", padx=10, pady=5)

    text_chat = tk.Text(panel_chat, state="disabled", wrap="word", bg="#FAFAFA", font=("Segoe UI", 10))
    text_chat.pack(padx=10, pady=(0, 5), fill="both", expand=True)

    def cargar_mensajes(event):
        seleccion = lista_contactos.curselection()
        if seleccion:
            idx = seleccion[0]
            usuario_destino_id, nombre_contacto = contactos_dict[idx]
            mensajes = obtener_mensajes(usuario_id, usuario_destino_id)
            text_chat.config(state="normal")
            text_chat.delete("1.0", tk.END)
            for m in mensajes:
                remitente = "Tú" if m[1] == usuario_id else nombre_contacto
                contenido = m[3]
                text_chat.insert(tk.END, f"{remitente}: {contenido}\n")
            text_chat.config(state="disabled")

    lista_contactos.bind("<<ListboxSelect>>", cargar_mensajes)

    frame_mensaje = tk.Frame(panel_chat, bg="white")
    frame_mensaje.pack(fill="x", padx=10, pady=5)

    entry_mensaje = tk.Entry(frame_mensaje, font=("Segoe UI", 10))
    entry_mensaje.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=4)

    def registrar_mensaje(remitente_id, destinatario_id, mensajeTexto):
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_EnviarMensaje ?, ?, ?", remitente_id, destinatario_id, mensajeTexto)
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el mensaje: {e}")

    def enviar_mensaje():
        mensaje = entry_mensaje.get().strip()
        if not mensaje:
            return
        seleccion = lista_contactos.curselection()
        if not seleccion:
            messagebox.showwarning("Selecciona un contacto", "Debes seleccionar un contacto antes de enviar un mensaje.")
            return
        idx = seleccion[0]
        usuario_destino_id, nombre_contacto = contactos_dict[idx]
        registrar_mensaje(usuario_id, usuario_destino_id, mensaje)
        entry_mensaje.delete(0, tk.END)
        cargar_mensajes(None)

    tk.Button(frame_mensaje, text="Enviar", bg="#0D6EFD", fg="white",
              font=("Segoe UI", 10, "bold"), command=enviar_mensaje).pack(side="right", padx=(5, 0))

def cerrar_sesion():
    global usuario_id, ventana_chat
    confirmacion = messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que deseas cerrar sesión?")
    if confirmacion:
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("EXEC sp_CerrarSesion @param_UsuarioID = ?", usuario_id)
            conexion.commit()
            if ventana_chat:
                ventana_chat.destroy()
            messagebox.showinfo("Sesión cerrada", "Has cerrado sesión exitosamente.")
        except pyodbc.Error as e:
            messagebox.showerror("Error al cerrar sesión", f"No se pudo cerrar la sesión:\n{e}")
        finally:
            if 'conexion' in locals():
                conexion.close()

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

tk.Button(frame, text="¿Ya tienes una cuenta? Iniciar Sesión", bg="white", fg="#0D6EFD", bd=0,
          font=("Segoe UI", 9, "bold"), command=mostrar_login).pack()

ventana.mainloop()
