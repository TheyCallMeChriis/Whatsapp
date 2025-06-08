from datetime import datetime, timedelta
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

# Calcular la fecha y hora de hace 1 minuto
un_minuto_atras = datetime.now() - timedelta(minutes=1)

# Replicar Usuario actualizado
sql_cursor.execute("""
    SELECT UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado
    FROM Usuario
    WHERE Actualizado >= ?
""", (un_minuto_atras,))
for row in sql_cursor.fetchall():
    row = tuple(row)  # Convertir a tupla
    try:
        mysql_cursor.execute("""
            INSERT INTO Usuario (UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                Nombre=VALUES(Nombre),
                Apellido=VALUES(Apellido),
                Contrasenna=VALUES(Contrasenna),
                Correo=VALUES(Correo),
                Estado=VALUES(Estado),
                NumeroTelefono=VALUES(NumeroTelefono),
                Actualizado=VALUES(Actualizado)
        """, row)
    except Exception as e:
        print(f"Error al insertar/actualizar Usuario: {e}")

# Replicar Mensaje actualizado
sql_cursor.execute("""
    SELECT MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado
    FROM Mensaje
    WHERE Actualizado >= ?
""", (un_minuto_atras,))
for row in sql_cursor.fetchall():
    row = tuple(row)  # Convertir a tupla
    try:
        mysql_cursor.execute("""
            INSERT INTO Mensaje (MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                MensajeEncriptado=VALUES(MensajeEncriptado),
                FechaEnvio=VALUES(FechaEnvio),
                Actualizado=VALUES(Actualizado)
        """, row)
    except Exception as e:
        print(f"Error al insertar/actualizar Mensaje: {e}")

# Replicar Sesion (sin campo 'Actualizado', usando 'FechaInicio' para determinar las nuevas sesiones)
sql_cursor.execute("""
    SELECT SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa
    FROM Sesion
    WHERE FechaInicio >= ?
""", (un_minuto_atras,))
for row in sql_cursor.fetchall():
    row = tuple(row)  # Convertir a tupla
    try:
        mysql_cursor.execute("""
            INSERT INTO Sesion (SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                FechaFin=VALUES(FechaFin),
                Activa=VALUES(Activa)
        """, row)
    except Exception as e:
        print(f"Error al insertar/actualizar Sesion: {e}")

# Commit para guardar cambios
mysql_conn.commit()

print("✅ Replicación diferencial ejecutada correctamente.")

# Cerrar las conexiones
sql_conn.close()
mysql_conn.close()
