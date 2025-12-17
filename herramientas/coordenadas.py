# coordenadas.py
import pyautogui
import time
import os

print("--- HERRAMIENTA DE CALIBRACIÓN ---")
print("Mueve el mouse a la ESQUINA SUPERIOR IZQUIERDA de donde aparecen los enemigos en la Battle List.")
print("Tienes 5 segundos...")
time.sleep(5)
x1, y1 = pyautogui.position()
print(f"Esquina 1 capturada: ({x1}, {y1})")

print("\nAhora mueve el mouse a la ESQUINA INFERIOR DERECHA del área donde saldría el PRIMER enemigo.")
print("(Imagina un rectángulo alrededor del nombre del primer enemigo)")
print("Tienes 5 segundos...")
time.sleep(5)
x2, y2 = pyautogui.position()
print(f"Esquina 2 capturada: ({x2}, {y2})")

ancho = x2 - x1
alto = y2 - y1

print("\n" + "="*40)
print("COPIA Y PEGA ESTO EN TU CÓDIGO:")
print(f'region_battle = {{"left": {x1}, "top": {y1}, "width": {ancho}, "height": {alto}}}')
print("="*40)