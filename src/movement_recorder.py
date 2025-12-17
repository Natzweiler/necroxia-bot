import keyboard
import time
import json
import threading
import pygetwindow as gw
import time
import pyautogui

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
        print(f"Grabación finalizada. Total pasos: {len(self.ruta)}")
        self.guardar_ruta()

    def guardar_ruta(self, archivo="ruta_cavebot.json"):
        with open(archivo, "w") as f:
            json.dump(self.ruta, f, indent=4)
        print(f"Ruta guardada en {archivo}")

    def reproducir_ruta(self, archivo="ruta_cavebot.json", callback_enemigo=None):           
        print("Reproduciendo ruta")
        with open(archivo, "r") as f:
            pasos = json.load(f)
        # Asegurarse de que la ventana del juego este activa para que no se presione en otras pantallas
        try:
            juego_ventana = gw.getWindowsWithTitle("Necroxia Origin")[0]
        except:
            print("Ventana del juego no encontrada. Asegúrate de que 'Necroxia Origin' esté abierto.")
            return
        for i, paso in enumerate (pasos):
            if keyboard.is_pressed('esc'):
                print("Reproducción detenida por el usuario.")
                keyboard.release(paso['tecla'])
                return False
            if callback_enemigo:
                pos_enemigo = callback_enemigo()
                if pos_enemigo:
                    print("Enemigo detectado, deteniendo reproducción.")
                    keyboard.release(paso['tecla'])
                    
                    pyautogui.click(pos_enemigo[0], pos_enemigo[1])
                    
                    while callback_enemigo():
                        if keyboard.is_pressed('esc'): return False
                        time.sleep(1) #espera a que el enemigo desaparezca
                    
                        pyautogui.click(juego_ventana.left +50, juego_ventana.top +50) #click fuera del battlelist para cerrar
            if not juego_ventana.isActive:
                print("Juego en segundo plano.")
                
                while not juego_ventana.isActive:
                    time.sleep(1) #espera a que la ventana se active
                print("Juego activo, continuando reproducción.")
                time.sleep(0.5)    
                    
                    
                    
            #Ejecuta el paso        
           # print(f"Caminando: {paso['tecla']}") se comento esta linea para evitar spam en consola
            keyboard.press(paso['tecla'])
            time.sleep(paso['duracion'])
            keyboard.release(paso['tecla'])
            
            #pausa entre pasos para evitar solapamientos
            time.sleep(0.1)
        return True

        