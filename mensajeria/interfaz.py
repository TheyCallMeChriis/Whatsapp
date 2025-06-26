import tkinter as tk
from tkinter import messagebox
from autentication import registrar_usuario, iniciar_sesion, cerrar_sesion
from mensajeria import obtener_usuarios, obtener_mensajes, registrar_mensaje
from datetime import datetime

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
    ventana.configure(bg="#8f949a")
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

    tk.Label(frame, text="🔐 Contraseña", font=("Segoe UI", 10), fg="#374151", bg="white").pack(anchor="w")
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

    tk.Button(frame, text="Registrarte", bg="#C3299C", fg="white", activebackground="#81366E",
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

    tk.Label(frame, text="🔐 Contraseña", font=("Segoe UI", 10), bg="white").pack(anchor="w")
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
        bg="#C3299C",
        fg="white",
        activebackground="#1f2937",
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
    global ventana_chat, canvas_chat, scroll_frame, lista_contactos, contactos_dict, entry_mensaje

    ventana_chat = tk.Toplevel(ventana)
    ventana_chat.title("Chat Principal")
    ventana_chat.geometry("1000x700")
    ventana_chat.configure(bg="#111b21")
    centrar_ventana(ventana_chat)

    menubar = tk.Menu(ventana_chat)
    cuenta_menu = tk.Menu(menubar, tearoff=0)
    cuenta_menu.add_command(label="Cerrar sesión", command=cerrar_sesion_usuario)
    menubar.add_cascade(label="Inicio", menu=cuenta_menu)
    ventana_chat.config(menu=menubar)

    frame_principal = tk.Frame(ventana_chat, bg="#111b21")
    frame_principal.pack(fill="both", expand=True)

    panel_contactos = tk.Frame(frame_principal, bg="#2a2f32", width=300)
    panel_contactos.pack(side="left", fill="y")
    panel_contactos.pack_propagate(False)

    tk.Label(panel_contactos, text="Chats", font=("Segoe UI", 16, "bold"),
             bg="#2a2f32", fg="#e9edef", pady=15).pack(anchor="w", padx=20)

    lista_contactos = tk.Listbox(panel_contactos, font=("Segoe UI", 11), bg="#2a2f32", fg="#e9edef",
                                 highlightthickness=0, bd=0, selectbackground="#3b4a54", selectforeground="#ffffff",
                                 activestyle="none")
    lista_contactos.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    usuarios = obtener_usuarios(usuario_id)
    contactos_dict = {}

    for idx, usuario in enumerate(usuarios):
        nombre_completo = f"{usuario.Nombre} {usuario.Apellido}"
        lista_contactos.insert(tk.END, f"  👤 {nombre_completo}")
        contactos_dict[idx] = (usuario.UsuarioID, nombre_completo)

    panel_chat = tk.Frame(frame_principal, bg="#0b141a")
    panel_chat.pack(side="right", fill="both", expand=True)

    frame_mensajes = tk.Frame(panel_chat, bg="#0b141a")
    frame_mensajes.pack(fill="both", expand=True, padx=10, pady=(10, 0))

    canvas_chat = tk.Canvas(frame_mensajes, bg="#0b141a", highlightthickness=0)
    scroll_frame = tk.Frame(canvas_chat, bg="#0b141a")
    scrollbar = tk.Scrollbar(frame_mensajes, orient="vertical", command=canvas_chat.yview)
    canvas_chat.configure(yscrollcommand=scrollbar.set)

    canvas_chat.create_window((0, 0), window=scroll_frame, anchor='nw')
    canvas_chat.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame.bind("<Configure>", lambda e: canvas_chat.configure(scrollregion=canvas_chat.bbox("all")))

    frame_input = tk.Frame(panel_chat, bg="#202c33", height=60)
    frame_input.pack(fill="x")
    frame_input.pack_propagate(False)

    entry_mensaje = tk.Entry(frame_input, font=("Segoe UI", 11), bg="#2a3942", fg="#e9edef",
                             relief="flat", insertbackground="#e9edef")
    entry_mensaje.pack(side="left", fill="x", expand=True, ipady=6, padx=(10, 5))

    btn_enviar = tk.Button(frame_input, text="➤", font=("Segoe UI", 12, "bold"), fg="white",
                           bg="#005c4b", relief="flat", command=enviar)
    btn_enviar.pack(side="right", padx=10)
    btn_enviar.configure(cursor="hand2", activebackground="#004a3c")

    # Bindings
    entry_mensaje.bind("<Return>", lambda e: (enviar(), "break"))
    lista_contactos.bind("<<ListboxSelect>>", cargar_mensajes)

def crear_burbuja_mensaje(parent, texto, es_propio, remitente="", fecha_envio=None):
    hora = fecha_envio.strftime("%H:%M") if fecha_envio else datetime.now().strftime("%H:%M")
    
    container = tk.Frame(parent, bg="#0b141a")
    container.pack(fill="x", pady=5, padx=10)

    alineador = tk.Frame(container, bg="#0b141a")
    alineador.pack(fill="x")

    
    max_width = 500

    if es_propio:
        burbuja = tk.Frame(alineador, bg="#005c4b", padx=10, pady=5)
        burbuja.pack(anchor="e", padx=(100, 10))  
    else:
        burbuja = tk.Frame(alineador, bg="#202c33", padx=10, pady=5)
        burbuja.pack(anchor="w", padx=(10, 100))  

    if remitente:
        tk.Label(
            burbuja,
            text=remitente,
            bg=burbuja["bg"],
            fg="#c0f5e2" if es_propio else "#8db2cc",
            font=("Segoe UI", 8, "bold"),
            wraplength=max_width,
            justify="left"
        ).pack(anchor="e" if es_propio else "w")

    tk.Label(
        burbuja,
        text=texto,
        bg=burbuja["bg"],
        fg="white",
        wraplength=max_width,  
        justify="left",
        font=("Segoe UI", 10)
    ).pack(anchor="e" if es_propio else "w")

    tk.Label(
        burbuja,
        text=hora,
        bg=burbuja["bg"],
        fg="#b0d6c7" if es_propio else "#98a7af",
        font=("Segoe UI", 7)
    ).pack(anchor="e")

def cargar_mensajes(event):
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    seleccion = lista_contactos.curselection()
    if seleccion:
        idx = seleccion[0]
        usuario_destino_id, nombre_contacto = contactos_dict[idx]
        mensajes = obtener_mensajes(usuario_id, usuario_destino_id)

        for m in mensajes:
            es_propio = m[1] == usuario_id
            remitente = "Tú" if es_propio else nombre_contacto
            crear_burbuja_mensaje(scroll_frame, m[3], es_propio, remitente, m[5])

        canvas_chat.update_idletasks()
        canvas_chat.yview_moveto(1)

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

def cerrar_sesion_usuario():
    global ventana_chat, usuario_id
    if messagebox.askyesno("Cerrar sesión", "¿Estás seguro?"):
        cerrar_sesion(usuario_id)
        if ventana_chat:
            ventana_chat.destroy()
        messagebox.showinfo("Sesión cerrada", "Has cerrado sesión correctamente.")