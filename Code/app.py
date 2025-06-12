from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# --------------------- CONEXIÓN BD ---------------------
def conectar_bd():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=MensajeriaBD;"
        "Trusted_Connection=yes;"
    )

@app.route("/")
def home():
    return "Bienvenido a la API de Mensajería"


# --------------------- ENDPOINT: Registro ---------------------
@app.route("/api/usuarios/registro", methods=["POST"])
def registrar_usuario():
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    telefono = data.get("telefono")
    contrasena = data.get("contrasena")

    if not all([nombre, apellido, correo, telefono, contrasena]):
        return jsonify({"error": "Faltan campos"}), 400

    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_RegistrarUsuario ?, ?, ?, ?, ?", 
                    nombre, apellido, contrasena, correo, telefono)
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado correctamente"})
    except pyodbc.IntegrityError:
        return jsonify({"error": "Correo o teléfono ya registrado"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- ENDPOINT: Login ---------------------
@app.route("/api/usuarios/login", methods=["POST"])
def login_usuario():
    data = request.json
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_LoginUsuario ?, ?", correo, contrasena)
        resultado = cursor.fetchone()

        if resultado:
            columnas = [col[0] for col in cursor.description]
            usuario = dict(zip(columnas, resultado))
            return jsonify(usuario)
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- ENDPOINT: Obtener Usuarios ---------------------
@app.route("/api/usuarios", methods=["GET"])
def obtener_usuarios():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerUsuarios")
        usuarios = cursor.fetchall()
        columnas = [col[0] for col in cursor.description]
        resultado = [dict(zip(columnas, u)) for u in usuarios]
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- ENDPOINT: Obtener Mensajes ---------------------
@app.route("/api/mensajes", methods=["GET"])
def obtener_mensajes():
    origen_id = request.args.get("origen_id")
    destino_id = request.args.get("destino_id")

    if not (origen_id and destino_id):
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerMensajes ?, ?", origen_id, destino_id)
        mensajes = cursor.fetchall()
        columnas = [col[0] for col in cursor.description]
        resultado = [dict(zip(columnas, m)) for m in mensajes]
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- ENDPOINT: Enviar Mensaje ---------------------
@app.route("/api/mensajes", methods=["POST"])
def enviar_mensaje():
    data = request.json
    remitente_id = data.get("remitente_id")
    destinatario_id = data.get("destinatario_id")
    mensaje = data.get("mensaje")

    if not all([remitente_id, destinatario_id, mensaje]):
        return jsonify({"error": "Faltan campos"}), 400

    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EnviarMensaje ?, ?, ?", remitente_id, destinatario_id, mensaje)
        conn.commit()
        return jsonify({"mensaje": "Mensaje enviado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- MAIN ---------------------
if __name__ == "__main__":
    app.run(debug=True)
