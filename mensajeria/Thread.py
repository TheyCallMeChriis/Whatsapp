# Thread.py
import threading
import time

class HiloReplicacion:
    def __init__(self, replicacion_obj, intervalo_segundos=10):
        self.replicacion = replicacion_obj
        self.intervalo = intervalo_segundos
        self.hilo = threading.Thread(target=self._ejecutar, daemon=True)
        self._detener = threading.Event()

    def _ejecutar(self):
        while not self._detener.is_set():
            self.replicacion.replicar()
            time.sleep(self.intervalo)

    def iniciar(self):
        self.hilo.start()

    def detener(self):
        self._detener.set()
        self.hilo.join()
