# replicacion_diferencial_Msql.py
from datetime import datetime, timedelta
import pyodbc
import mysql.connector

class ReplicacionDiferencialMySQLtoSQL:
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

            print("🔄 Iniciando replicación diferencial MySQL → SQL Server...")

            un_minuto_atras = datetime.now() - timedelta(minutes=1)

            # Replicar Usuario
            mysql_cursor.execute("""
                SELECT UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado
                FROM Usuario
                WHERE Actualizado >= %s
            """, (un_minuto_atras,))
            for row in mysql_cursor.fetchall():
                datos = tuple(row)
                try:
                    sql_cursor.execute("""
                        MERGE INTO Usuario AS target
                        USING (SELECT ? AS UsuarioID) AS source
                        ON target.UsuarioID = source.UsuarioID
                        WHEN MATCHED THEN
                            UPDATE SET Nombre=?, Apellido=?, Contrasenna=?, Correo=?, Estado=?, NumeroTelefono=?, Actualizado=?
                        WHEN NOT MATCHED THEN
                            INSERT (UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """, datos[0:1] + datos[1:] + datos)
                except Exception as e:
                    print(f"❌ Error al replicar Usuario: {e}")

            # Replicar Mensaje
            mysql_cursor.execute("""
                SELECT MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado
                FROM Mensaje
                WHERE Actualizado >= %s
            """, (un_minuto_atras,))
            sql_cursor.execute("SET IDENTITY_INSERT Mensaje ON")
            for row in mysql_cursor.fetchall():
                datos = tuple(row)
                try:
                    sql_cursor.execute("""
                        MERGE INTO Mensaje AS target
                        USING (SELECT ? AS MensajeID) AS source
                        ON target.MensajeID = source.MensajeID
                        WHEN MATCHED THEN
                            UPDATE SET EmisorID=?, ReceptorID=?, MensajeEncriptado=?, FechaEnvio=?, Actualizado=?
                        WHEN NOT MATCHED THEN
                            INSERT (MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado)
                            VALUES (?, ?, ?, ?, ?, ?);
                    """, datos[0:1] + datos[1:] + datos)
                except Exception as e:
                    print(f"❌ Error al replicar Mensaje: {e}")
            sql_cursor.execute("SET IDENTITY_INSERT Mensaje OFF")

            # Replicar Sesion
            mysql_cursor.execute("""
                SELECT SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa
                FROM Sesion
                WHERE FechaInicio >= %s
            """, (un_minuto_atras,))
            sql_cursor.execute("SET IDENTITY_INSERT Sesion ON")
            for row in mysql_cursor.fetchall():
                datos = tuple(row)
                try:
                    sql_cursor.execute("""
                        MERGE INTO Sesion AS target
                        USING (SELECT ? AS SesionID) AS source
                        ON target.SesionID = source.SesionID
                        WHEN MATCHED THEN
                            UPDATE SET UsuarioID=?, Token=?, FechaInicio=?, FechaFin=?, Activa=?
                        WHEN NOT MATCHED THEN
                            INSERT (SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa)
                            VALUES (?, ?, ?, ?, ?, ?);
                    """, datos[0:1] + datos[1:] + datos)
                except Exception as e:
                    print(f"❌ Error al replicar Sesión: {e}")
            sql_cursor.execute("SET IDENTITY_INSERT Sesion OFF")

            sql_conn.commit()
            print("✅ Replicación diferencial MySQL → SQL Server ejecutada correctamente.")

        except Exception as e:
            print(f"⚠ Error general en replicación diferencial: {e}")

        finally:
            try:
                mysql_conn.close()
                sql_conn.close()
            except:
                pass