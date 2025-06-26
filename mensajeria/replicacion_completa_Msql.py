import pyodbc
import mysql.connector

class ReplicacionMySQLtoSQL:
    def replicar(self):
        try:
            
            mysql_conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="MensajeriaReplica"
            )
            mysql_cursor = mysql_conn.cursor()

            
            sql_conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=MensajeriaBD;"
                "Trusted_Connection=yes"
            )
            sql_cursor = sql_conn.cursor()

            print("🔁 Iniciando replicación completa MySQL → SQL Server...")

            
            sql_cursor.execute("DELETE FROM Mensaje")
            sql_cursor.execute("DELETE FROM Sesion")
            sql_cursor.execute("DELETE FROM Usuario")

            
            mysql_cursor.execute("SELECT UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado FROM Usuario")
            usuarios = mysql_cursor.fetchall()

            sql_cursor.execute("SET IDENTITY_INSERT Usuario ON")
            for row in usuarios:
                try:
                    sql_cursor.execute("""
                        INSERT INTO Usuario (UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, row)
                except Exception as e:
                    print(f"❌ Error insertando Usuario: {e}")
            sql_cursor.execute("SET IDENTITY_INSERT Usuario OFF")

            
            mysql_cursor.execute("SELECT MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado FROM Mensaje")
            mensajes = mysql_cursor.fetchall()

            sql_cursor.execute("SET IDENTITY_INSERT Mensaje ON")
            for row in mensajes:
                try:
                    sql_cursor.execute("""
                        INSERT INTO Mensaje (MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, row)
                except Exception as e:
                    print(f"❌ Error insertando Mensaje: {e}")
            sql_cursor.execute("SET IDENTITY_INSERT Mensaje OFF")

            
            mysql_cursor.execute("SELECT SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa FROM Sesion")
            sesiones = mysql_cursor.fetchall()

            sql_cursor.execute("SET IDENTITY_INSERT Sesion ON")
            for row in sesiones:
                try:
                    sql_cursor.execute("""
                        INSERT INTO Sesion (SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, row)
                except Exception as e:
                    print(f"❌ Error insertando Sesion: {e}")
            sql_cursor.execute("SET IDENTITY_INSERT Sesion OFF")

            sql_conn.commit()
            print("✅ Replicación completa MySQL → SQL Server finalizada correctamente.")

        except Exception as e:
            print(f"❌ Error general en replicación completa MySQL → SQL Server: {e}")

        finally:
            try:
                mysql_conn.close()
                sql_conn.close()
            except:
                pass
