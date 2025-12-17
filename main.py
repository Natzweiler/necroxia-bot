from src.movement_recorder import Recorder
from src.vision import Vision
import time
import pyautogui

def main():
    # 1. Inicializamos las "clases" (Los planos de nuestros objetos)
    bot_vision = Vision()
    bot_movement = Recorder()

    # 2. DEFINIR ZONA DE BATALLA
    # Aquí pegas lo que te dio el script 'coordenadas.py'.
    # Ejemplo (estos son números inventados, pon los tuyos):
    region_battle = {"left": 1505, "top": 187, "width": 167, "height": 15}

    # 3. Definimos la función de ataque
    # Esta función se la pasaremos al robot para que la use mientras camina.
    
    def checar_si_hay_enemigo():
        # Tomamos la captura
        img = pyautogui.screenshot(region=(
            region_battle['left'], 
            region_battle['top'], 
            region_battle['width'], 
            region_battle['height']
        ))
        
        # --- CORRECCIÓN AQUÍ ---
        # Convertimos la imagen a Escala de Grises ('L') 
        # Esto hace que los pixeles sean números simples (0-255) en vez de trios (R,G,B)
        img = img.convert('L')  
        # -----------------------

        # Ahora el resto del código matemático funcionará perfecto
        colores = list(img.getdata())
        
        if not colores: # Seguridad por si la lista está vacía
            return None

        max_color = max(colores) 
        min_color = min(colores) 
        diferencia = max_color - min_color
        
        # UMBRAL:
        if diferencia > 10: 
            center_x = region_battle['left'] + (region_battle['width'] // 2)
            center_y = region_battle['top'] + (region_battle['height'] // 2)
            return (center_x, center_y)
        
        return None

    # 4. Interfaz de Usuario (Consola)
    print("--- NECROXIA BOT v1.0 ---")
    print(f"Zona de batalla configurada: {region_battle}")
    opcion = input("1. Grabar Ruta\n2. Iniciar Cavebot\nElige: ")

    if opcion == "1":
        bot_movement.iniciar_grabacion()
    
    elif opcion == "2":
        print("Iniciando en 3 segundos... (NO MUEVAS LA VENTANA DE BATTLE)")
        time.sleep(3)
        while True:
            # Enviamos la función 'checar_si_hay_enemigo' dentro de la ruta
            termino = bot_movement.reproducir_ruta(callback_enemigo=checar_si_hay_enemigo)
            
            if not termino: # Si el usuario presionó ESC
                print("Bot detenido.")
                break

if __name__ == "__main__":
    main()