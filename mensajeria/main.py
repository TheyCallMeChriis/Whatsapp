# main.py

from interfaz import iniciar_interfaz
from replica_completa import Replicacion
from replica_diferencial import ReplicacionDiferencial
from Thread import HiloReplicacion
import time
import threading

if __name__ == "__main__":
    
    replicacion_completa = Replicacion()
    replicacion_diferencial = ReplicacionDiferencial()

    hilo_completo = HiloReplicacion(replicacion_completa, intervalo_segundos=30)
    hilo_diferencial = HiloReplicacion(replicacion_diferencial, intervalo_segundos=10)

    hilo_completo.iniciar()
    hilo_diferencial.iniciar()

    try:
        iniciar_interfaz()
    except KeyboardInterrupt:
        print("🛑 Interfaz interrumpida manualmente.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Deteniendo hilos de replicación...")
        hilo_completo.detener()
        hilo_diferencial.detener()
        print("✅ Programa finalizado.")
