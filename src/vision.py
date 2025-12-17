
import cv2
import numpy as np
import mss
import pygetwindow as gw

class Vision:
    def __init__(self, window_title="Necroxia Origin"):
        self.window_title = window_title
        self.monitor = self._get_window_geometry()

    def _get_window_geometry(self):
        # Busca la ventana del juego para limitar el área de visión
        try:
            window = gw.getWindowsWithTitle(self.window_title)[0]
            return {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
        except IndexError:
            print(f"Ventana '{self.window_title}' no encontrada. Usando pantalla completa.")
            return {"top": 0, "left": 0, "width": 1920, "height": 1080}

    def get_screenshot(self):
        with mss.mss() as sct:
            img = np.array(sct.grab(self.monitor))
            # MSS devuelve BGRA, OpenCV usa BGR. Quitamos el canal Alpha.
            img = img[:, :, :3] 
            return img

    def find_template(self, screenshot, template_path, threshold=0.8):
        # Lógica de Template Matching aquí
        # Retorna las coordenadas (x, y) si encuentra la imagen
        pass
    
    def buscar_enemigo(self):
        #logica para capturar pantalla
        screen = self.get_screenshot()
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        #logica para buscar enemigo
        #debemos tener una imagen de referencia del enemigo en los assets llamada battle_icon.png
        
        #ajustamos manualmente el battlelist 
        x,y,w,h = 1740, 50 , 150, 40
        
        recorte_battle = screen[y:y+h, x:x+w]
        std_dev = np.std(recorte_battle)
        if std_dev > 5: #umbral para detectar cambios
            return (x+w//2, y+h//2) #retorna el centro del area del battlelist
        return None