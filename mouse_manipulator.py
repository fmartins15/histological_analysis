#Made by Felipe Meier Martins
#Collab PET EEL - LPDS
#----------------------------------------------------------
'''
Arquivo destinado para obtenção das coordenadas atualizadas do mouse
'''
from pynput.mouse import Controller

def mouse_position(): #função para posição do mouse
    mouse = Controller()
    position = mouse.position
    x = position[0]
    y = position[1]
    return x, y
