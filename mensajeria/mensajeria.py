from bd import conectar_bd

def obtener_usuarios():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerUsuarios")
        return cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return []
    finally:
        conn.close()

def obtener_mensajes(usuario_origen_id, usuario_destino_id):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerMensajes ?, ?", usuario_origen_id, usuario_destino_id)
        return cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return []
    finally:
        conn.close()

def registrar_mensaje(remitente_id, destinatario_id, mensaje):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EnviarMensaje ?, ?, ?", remitente_id, destinatario_id, mensaje)
        conn.commit()
    except Exception as e:
        print("Error al enviar mensaje:", e)
    finally:
        conn.close()