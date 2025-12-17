# src/movement_recorder.py
import keyboard
import time
import json
import threading

class Recorder:
    def __init__(self):
        self.ruta = [] #registro de pasos
        self.grabando = False
        self.inicio_paso = 0

    def iniciar_grabacion(self):
        self.ruta = []
        self.grabando = True
        print("Rec iniciado (Camina con las flechas. Presiona 'Esc' para terminar)")
        
        
        keyboard.hook(self._registrar_evento)
        keyboard.wait('esc') #el teclado espera hasta el esc para detener la grabacion
        
        self.detener_grabacion()

    def _registrar_evento(self, evento):
        if not self.grabando: return
        if evento.name == 'esc': return


        if evento.event_type == 'down':
            if self.inicio_paso == 0:
                self.inicio_paso = time.time()
        
        elif evento.event_type == 'up':
            if self.inicio_paso != 0:
                duracion = time.time() - self.inicio_paso
                paso = {
                    "tecla": evento.name,
                    "duracion": round(duracion, 3) #precison del registro
                }
                if duracion > 0.05: #no registra toques accidentales muy cortos
                    self.ruta.append(paso)
                    print(f"Paso registrado: {paso['tecla']} por {paso['duracion']}s")
                self.inicio_paso = 0

    def detener_grabacion(self):
        self.grabando = False
        keyboard.unhook_all()
        print(f"⏹️ Grabación finalizada. Total pasos: {len(self.ruta)}")
        self.guardar_ruta()

    def guardar_ruta(self, archivo="ruta_cavebot.json"):
        with open(archivo, "w") as f:
            json.dump(self.ruta, f, indent=4)
        print(f"💾 Ruta guardada en {archivo}")

    def reproducir_ruta(self, archivo="ruta_cavebot.json"):
        print("Reproduciendo ruta")
        with open(archivo, "r") as f:
            pasos = json.load(f)
        
        for paso in pasos:

            print(f"Caminando: {paso['tecla']}")
            keyboard.press(paso['tecla'])
            time.sleep(paso['duracion'])
            keyboard.release(paso['tecla'])
            
            #pausa entre pasos para evitar solapamientos
            time.sleep(0.1)

if __name__ == "__main__":
    rec = Recorder()
    accion = input("(1: Grabar, 2: Reproducir): ")
    
    if accion == "1":
        rec.iniciar_grabacion()
    elif accion == "2":
        print("Cambiando al juego en 3 segundos...") #tienes que cambiar de ventana porque sino se mueve en la ventana que esteusando
        time.sleep(3)
        while True: # repetir ruta solo para pruebas
            rec.reproducir_ruta()
    if accion == "3":
        print("Saliendo...")
        exit()
        