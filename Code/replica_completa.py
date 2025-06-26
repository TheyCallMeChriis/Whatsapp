import pyodbc
import mysql.connector

# Conexión a SQL Server (Windows Authentication)
sql_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=MensajeriaBD;"
    "Trusted_Connection=yes"
)
sql_cursor = sql_conn.cursor()

# Conexión a MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="27186627",
    database="MensajeriaReplica"
)
mysql_cursor = mysql_conn.cursor()

# Borrar datos (orden: dependientes primero)
mysql_cursor.execute("DELETE FROM Mensaje")
mysql_cursor.execute("DELETE FROM Sesion")
mysql_cursor.execute("DELETE FROM Usuario") 

# Replicar Usuario
sql_cursor.execute("SELECT UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado FROM Usuario")
usuarios = sql_cursor.fetchall()
for row in usuarios:
    row = tuple(row)  # Convertir la fila a tupla
    try:
        print(f"Insertando Usuario: {row}")
        mysql_cursor.execute("""
            INSERT INTO Usuario (UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, row)
    except Exception as e:
        print(f"Error al insertar Usuario: {e}")

# Replicar Mensaje
sql_cursor.execute("SELECT MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado FROM Mensaje")
mensajes = sql_cursor.fetchall()
for row in mensajes:
    row = tuple(row)  # Convertir la fila a tupla
    try:
        print(f"Insertando Mensaje: {row}")
        mysql_cursor.execute("""
            INSERT INTO Mensaje (MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, row)
    except Exception as e:
        print(f"Error al insertar Mensaje: {e}")

# Replicar Sesion
sql_cursor.execute("SELECT SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa FROM Sesion")
sesiones = sql_cursor.fetchall()
for row in sesiones:
    row = tuple(row)  # Convertir la fila a tupla
    try:
        print(f"Insertando Sesion: {row}")
        mysql_cursor.execute("""
            INSERT INTO Sesion (SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, row)
    except Exception as e:
        print(f"Error al insertar Sesion: {e}")

mysql_conn.commit()
print("✅ Replicación completa ejecutada correctamente.")
sql_conn.close()
mysql_conn.close()
