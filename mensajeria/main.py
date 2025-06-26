from interfaz import iniciar_interfaz
from replica_completa import Replicacion
from replica_diferencial import ReplicacionDiferencial
from replicacion_completa_Msql import ReplicacionMySQLtoSQL
from replicacion_diferencial_Msql import ReplicacionDiferencialMySQLtoSQL
from Thread import HiloReplicacion
import time

if __name__ == "__main__":
   
    rep_sql_mysql = Replicacion()
    rep_dif_sql_mysql = ReplicacionDiferencial()
    rep_mysql_sql = ReplicacionMySQLtoSQL()
    rep_dif_mysql_sql = ReplicacionDiferencialMySQLtoSQL()

    
    hilo1 = HiloReplicacion(rep_sql_mysql, intervalo_segundos=60)
    hilo2 = HiloReplicacion(rep_dif_sql_mysql, intervalo_segundos=20)
    hilo3 = HiloReplicacion(rep_mysql_sql, intervalo_segundos=60)
    hilo4 = HiloReplicacion(rep_dif_mysql_sql, intervalo_segundos=20)

    hilo1.iniciar()
    hilo2.iniciar()
    hilo3.iniciar()
    hilo4.iniciar()

    
    try:
        iniciar_interfaz()
    except KeyboardInterrupt:
        print("🛑 Interfaz interrumpida manualmente.")

    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Deteniendo hilos de replicación...")
        hilo1.detener()
        hilo2.detener()
        hilo3.detener()
        hilo4.detener()
        print("✅ Programa finalizado.")