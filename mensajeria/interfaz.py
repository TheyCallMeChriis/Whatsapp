import tkinter as tk
from tkinter import messagebox
from autentication import registrar_usuario, iniciar_sesion, cerrar_sesion
from mensajeria import obtener_usuarios, obtener_mensajes, registrar_mensaje

usuario_id = None
token = None
ventana_chat = None

def centrar_ventana(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

def iniciar_interfaz():
    global ventana
    ventana = tk.Tk()
    ventana.title("Registro")
    ventana.geometry("450x530")
    ventana.configure(bg="#f0f4f8")
    centrar_ventana(ventana)

    frame = tk.Frame(ventana, bg="white", padx=20, pady=20, bd=2, relief="groove")
    frame.pack(pady=30)

    tk.Label(frame, text="Regístrate", font=("Segoe UI", 18, "bold"), fg="#1e3a8a", bg="white").pack(pady=10)

    def crear_entrada(texto):
        tk.Label(frame, text=texto, font=("Segoe UI", 10), fg="#374151", bg="white").pack(anchor="w")
        entry = tk.Entry(frame, width=35, bg="#f9fafb", fg="#111827", insertbackground="#111827",
                         highlightthickness=1, highlightbackground="#d1d5db", relief="flat")
        entry.pack(pady=(0, 10))
        return entry

    entry_nombre = crear_entrada("👤 Nombre")
    entry_apellido = crear_entrada("👥 Apellido")
    entry_correo = crear_entrada("📧 Correo")
    entry_telefono = crear_entrada("📞 Teléfono")

    tk.Label(frame, text="🔒 Contraseña", font=("Segoe UI", 10), fg="#374151", bg="white").pack(anchor="w")
    entry_password = tk.Entry(frame, show="*", width=35, bg="#f9fafb", fg="#111827", insertbackground="#111827",
                              highlightthickness=1, highlightbackground="#d1d5db", relief="flat")
    entry_password.pack(pady=(0, 15))

    def registrar():
        registrar_usuario(
            entry_nombre.get(),
            entry_apellido.get(),
            entry_correo.get(),
            entry_telefono.get(),
            entry_password.get()
        )

    tk.Button(frame, text="Registrarte", bg="#1e3a8a", fg="white", activebackground="#3b82f6",
              activeforeground="white", width=30, font=("Segoe UI", 10, "bold"), bd=0,
              padx=10, pady=6, command=registrar).pack(pady=10)

    tk.Button(frame, text="¿Ya tienes una cuenta? Iniciar Sesión", bg="white", fg="#3b82f6", bd=0,
              font=("Segoe UI", 9, "bold"), cursor="hand2", command=mostrar_login).pack()

    ventana.mainloop()

def mostrar_login():
    login_win = tk.Toplevel(ventana)
    login_win.title("Iniciar sesión")
    login_win.geometry("450x380")
    login_win.configure(bg="#3b434a")
    centrar_ventana(login_win)

    frame = tk.Frame(login_win, bg="white", padx=20, pady=20, bd=2, relief="groove")
    frame.pack(pady=30)

    tk.Label(frame, text="Iniciar sesión", font=("Segoe UI", 16, "bold"), fg="#1d1ae4", bg="white").pack(pady=10)

    tk.Label(frame, text="📧 Correo electrónico", font=("Segoe UI", 10), bg="white").pack(anchor="w")
    entry_login_correo = tk.Entry(frame, width=35, bg="#f9fafb", fg="#111827", insertbackground="#111827",
                                  highlightthickness=1, highlightbackground="#d1d5db", relief="flat")
    entry_login_correo.pack(pady=(0, 10))

    tk.Label(frame, text="🔒 Contraseña", font=("Segoe UI", 10), bg="white").pack(anchor="w")
    entry_login_pass = tk.Entry(frame, show="*", width=35, bg="#f9fafb", fg="#111827", insertbackground="#111827",
                                highlightthickness=1, highlightbackground="#d1d5db", relief="flat")
    entry_login_pass.pack(pady=(0, 15))

    def login():
        global usuario_id, token
        resultado = iniciar_sesion(entry_login_correo.get(), entry_login_pass.get())
        if resultado and resultado.get("UsuarioID") and resultado.get("Token"):
            usuario_id = resultado["UsuarioID"]
            token = resultado["Token"]
            messagebox.showinfo("Bienvenido", f"Bienvenido usuario {usuario_id}")
            mostrar_interfaz_principal()
            login_win.destroy()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas o usuario no encontrado.")

    tk.Button(
    frame,
    text="Iniciar sesión",
    bg="#C3299C",            # Mismo fondo oscuro
    fg="white",              # Texto blanco
    activebackground="#1f2937",  # Color al presionar
    activeforeground="white",
    width=30,
    font=("Segoe UI", 10, "bold"),
    bd=0,
    padx=10,
    pady=6,
    cursor="hand2",
    command=login
).pack(pady=10)

def mostrar_interfaz_principal():
    global ventana_chat
    ventana_chat = tk.Toplevel(ventana)
    ventana_chat.title("Mensajería")
    ventana_chat.geometry("900x600")
    ventana_chat.configure(bg="#f0f4f8")
    centrar_ventana(ventana_chat)

    menubar = tk.Menu(ventana_chat)
    cuenta_menu = tk.Menu(menubar, tearoff=0)
    cuenta_menu.add_command(label="Cerrar sesión", command=cerrar_sesion_usuario)
    menubar.add_cascade(label="Inicio", menu=cuenta_menu)
    ventana_chat.config(menu=menubar)

    frame_principal = tk.Frame(ventana_chat, bg="#e5e7eb")
    frame_principal.pack(fill="both", expand=True)

    panel_contactos = tk.Frame(frame_principal, bg="white", width=250, bd=1, relief="sunken")
    panel_contactos.pack(side="left", fill="y")

    tk.Label(panel_contactos, text="Contactos", font=("Segoe UI", 12, "bold"), bg="white", fg="#1e3a8a").pack(pady=10)
    lista_contactos = tk.Listbox(panel_contactos, font=("Segoe UI", 10), width=30, bd=1, relief="solid")
    lista_contactos.pack(padx=10, pady=5, fill="y", expand=True)

    usuarios = obtener_usuarios()
    contactos_dict = {}

    for idx, usuario in enumerate(usuarios):
        nombre_completo = f"{usuario.Nombre} {usuario.Apellido}"
        lista_contactos.insert(tk.END, nombre_completo)
        contactos_dict[idx] = (usuario.UsuarioID, nombre_completo)

    panel_chat = tk.Frame(frame_principal, bg="white", bd=1, relief="sunken")
    panel_chat.pack(side="right", fill="both", expand=True)

    tk.Label(panel_chat, text=f"Usuario ID: {usuario_id}", font=("Segoe UI", 10), bg="white", anchor="w").pack(fill="x", padx=10, pady=5)

    text_chat = tk.Text(panel_chat, state="disabled", wrap="word", bg="#f9fafb", fg="#1f2937",
                        font=("Segoe UI", 10), bd=1, relief="solid")
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

    entry_mensaje = tk.Entry(frame_mensaje, font=("Segoe UI", 10), bg="#ffffff", fg="#111827",
                             highlightthickness=1, highlightbackground="#d1d5db", relief="flat")
    entry_mensaje.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=4)

    def enviar():
        mensaje = entry_mensaje.get().strip()
        if not mensaje:
            return
        seleccion = lista_contactos.curselection()
        if not seleccion:
            messagebox.showwarning("Selecciona un contacto", "Debes seleccionar un contacto.")
            return
        idx = seleccion[0]
        usuario_destino_id, _ = contactos_dict[idx]
        registrar_mensaje(usuario_id, usuario_destino_id, mensaje)
        entry_mensaje.delete(0, tk.END)
        cargar_mensajes(None)

    tk.Button(frame_mensaje, text="Enviar", bg="#3b82f6", fg="white",
              font=("Segoe UI", 10, "bold"), activebackground="#2563eb",
              bd=0, padx=10, pady=5, command=enviar).pack(side="right", padx=(5, 0))

def cerrar_sesion_usuario():
    global ventana_chat, usuario_id
    if messagebox.askyesno("Cerrar sesión", "¿Estás seguro?"):
        cerrar_sesion(usuario_id)
        if ventana_chat:
            ventana_chat.destroy()
        messagebox.showinfo("Sesión cerrada", "Has cerrado sesión correctamente.")