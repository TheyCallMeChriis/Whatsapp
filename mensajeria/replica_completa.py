# replica_completa.py
import pyodbc
import mysql.connector

class Replicacion:
    def replicar(self):
        try:
            
            sql_conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=MensajeriaBD;"
                "Trusted_Connection=yes"
            )
            sql_cursor = sql_conn.cursor()

            mysql_conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="MensajeriaReplica"
            )
            mysql_cursor = mysql_conn.cursor()

            
            mysql_cursor.execute("DELETE FROM Mensaje")
            mysql_cursor.execute("DELETE FROM Sesion")
            mysql_cursor.execute("DELETE FROM Usuario")

            
            sql_cursor.execute("""
                SELECT UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado FROM Usuario
            """)
            for row in sql_cursor.fetchall():
                datos = tuple(row)
                mysql_cursor.execute("""
                    INSERT INTO Usuario (UsuarioID, Nombre, Apellido, Contrasenna, Correo, Estado, NumeroTelefono, Actualizado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, datos)

           
            sql_cursor.execute("""
                SELECT MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado FROM Mensaje
            """)
            for row in sql_cursor.fetchall():
                datos = tuple(row)
                mysql_cursor.execute("""
                    INSERT INTO Mensaje (MensajeID, EmisorID, ReceptorID, MensajeEncriptado, FechaEnvio, Actualizado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, datos)

            
            sql_cursor.execute("""
                SELECT SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa FROM Sesion
            """)
            for row in sql_cursor.fetchall():
                datos = tuple(row)
                mysql_cursor.execute("""
                    INSERT INTO Sesion (SesionID, UsuarioID, Token, FechaInicio, FechaFin, Activa)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, datos)

            
            mysql_conn.commit()
            print("✅ Replicación completa ejecutada correctamente.")
        
        except Exception as e:
            print(f"❌ Error general en replicación completa: {e}")
        
        finally:
            try:
                sql_conn.close()
                mysql_conn.close()
            except:
                pass
