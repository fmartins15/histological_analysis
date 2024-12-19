# Made by Felipe Meier Martins
# Collab PET EEL - LPDS
# ----------------------------------------------------------
'''
Este arquivo contém a lógica para processamento de imagens em um ambiente digital que simula o laboratório de um patologista.
As funções incluem:
- Ajuste das dimensões da imagem ao tamanho do monitor.
- Aplicação de efeitos de opacidade.
- Aplicação do zoom (do arquivo zoom.py) e interação com o mouse.
- Armazenamento das coordenadas analisadas em um arquivo para análise posterior (arquivo data.py).
'''

import threading  # Biblioteca para execução de tarefas simultâneas (multithreading)
import cv2  # Biblioteca OpenCV para processamento de imagens
from mouse_manipulator import mouse_position  # Função externa para capturar a posição do mouse
import numpy as np  # Biblioteca para operações matemáticas eficientes
from screeninfo import get_monitors  # Função para obter informações do monitor
from time import perf_counter as pc  # Função para medir o tempo de execução
import time  # Biblioteca para manipulação de tempo
from zoom import centering  # Função externa que implementa zoom centralizado
from tkinter import *  # Biblioteca para criar interfaces gráficas (GUI)

# Variáveis globais para controle da interface e do zoom
x_gui=0
y_gui=0
current_zoom_level = 1

# Classe responsável pela manipulação da imagem
class Image():
    def __init__(self, path, width, height, blur,radius):
        self.path = path  # objeto de caminho da imagem
        self.width = width  # objeto de largura da imagem
        self.height = height  # objeto de altura da imagem
        self.blur = blur  # objeto de opacidade da imagem
        self.radius = radius #objeto de raio de circulo focal

        # Função que obtém as dimensões originais da imagem
    def get_image_dimension(self):  # função para receber dimensões da imagem
        im = cv2.imread(self.path)  # Carrega a imagem
        dimensions = im.shape  # Retorna as dimensões da imagem (altura, largura, canais)
        return dimensions


    # Função que redimensiona e aplica um filtro de desfoque na imagem
    def resize_image(self):  # função de processamento da imagem
        image_array = cv2.imread(self.path)  # Carrega a imagem
        resize_image = cv2.resize(image_array, (self.width, self.height))  # Redimensiona a imagem
        blur_image = cv2.blur(resize_image, self.blur)  # Aplica o filtro de desfoque
        return blur_image


# Instância inicial da classe Image
im_def = Image(path=0, width=0, height=0, blur=(0, 0), radius=80)  # recebimento dos parâmetro

# Função que obtém informações do monitor (resolução da tela)
def screen_info():
    for m in get_monitors():
        screen_width = m.width  # Largura do monitor
        screen_height = m.height  # Altura do monitor
    return screen_width, screen_height

# Flags e funções para alterar o raio da lupa
flag_change_radius = 0
def change_flag():
    global flag_change_radius
    flag_change_radius = 1

# Função para alterar o raio da lupa focal
def change_radius(desired_radius):
    global im_def
    im_def.radius = desired_radius  # Atualiza o raio da lupa
    print(f"Raio alterado para: {im_def.radius}")

# Função que exibe uma interface gráfica para seleção de zoom e ajuste do raio
def zoom_label(x, y, zoom_level):
    global flag_change_radius
    screen_width, screen_height = screen_info()  # Obtém as dimensões do monitor

    def apply_zoom(zoom_level):
        global current_zoom_level
        current_zoom_level = zoom_level # Atualiza o nível de zoom
        print("zoom mudado" + str(current_zoom_level))
        root.destroy()  # Fechar a janela após selecionar o zoom
        return current_zoom_level

    def open_radius_window():
        root.destroy()  # Fecha a janela de seleção de zoom
        root_radius = Toplevel()
        root_radius.geometry("300x300+{}+{}".format(x, y))  # Define a posição da nova janela
        root_radius.title("Alterar Raio da Lupa")

        label_radius = Label(root_radius, text="Selecione o raio da lupa:")
        label_radius.pack(pady=10)

        Button(root_radius, text="40px", padx=50, bg="blue",
               command=lambda: [change_radius(40), root_radius.destroy()]).pack(pady=5)
        Button(root_radius, text="60px", padx=50, bg="blue",
               command=lambda: [change_radius(60), root_radius.destroy()]).pack(pady=5)
        Button(root_radius, text="80px", padx=50, bg="blue",
               command=lambda: [change_radius(80), root_radius.destroy()]).pack(pady=5)
        Button(root_radius, text="100px", padx=50, bg="blue",
               command=lambda: [change_radius(100), root_radius.destroy()]).pack(pady=5)

        Button(root_radius, text="Cancelar", bg="red", command=root_radius.destroy).pack(pady=10)

        root_radius.grab_set()  # Bloqueia interação com outras janelas enquanto esta está aberta
        root_radius.wait_window()

    root = Toplevel()

    # Determine se a janela de zoom deve aparecer a direita  ou a esquerda do clique
    if x + 300 > screen_width:  # Se a janela ultrapassar a largura da tela
        x = x - 300  # Coloque a janela a esquerda do clique
    else:
        x = x  # Coloque a janela a direita do clique

    # Determine se a janela de zoom deve aparecer acima ou abaixo do clique
    if y + 300 > screen_height:  # Se a janela ultrapassar a altura da tela
        y = y - 300  # Coloque a janela acima do clique
    else:
        y= y  # Coloque a janela abaixo do clique

    root.geometry("300x300+{}+{}".format(x, y))  # Define a posição da janela
    root.title("Selecionar zoom")
    label = Label(root, text="Selecione um zoom")
    label.place(x=50, y=20)
    if zoom_level==1:
        button2x = Button(root, text="2X", padx=50, bg="blue", command=lambda: apply_zoom(2))
        button2x.place(x=50, y=50)

        button4x = Button(root, text="4X", padx=50, bg="blue", command=lambda: apply_zoom(4))
        button4x.place(x=50, y=70)

        button10x = Button(root, text="10X", padx=50, bg="blue", command=lambda: apply_zoom(10))
        button10x.place(x=50, y=90)

        button20x = Button(root, text="20X", padx=50, bg="blue", command=lambda: apply_zoom(20))
        button20x.place(x=50, y=110)

        button40x = Button(root, text="40X", padx=50, bg="blue", command=lambda: apply_zoom(40))
        button40x.place(x=50, y=130)

        button60x = Button(root, text="60X", padx=50, bg="blue", command=lambda: apply_zoom(60))
        button60x.place(x=50, y=150)

        button100x = Button(root, text="100X", padx=50, bg="blue", command=lambda: apply_zoom(100))
        button100x.place(x=50, y=170)

    button0x = Button(root, text="Voltar ao zoom original", bg="blue",command=lambda: apply_zoom(1))
    button0x.place(x=50, y=190)

    button_zoom_radius_adjust = Button(root, text="Alterar Raio da Lupa", bg="green", command=open_radius_window)
    button_zoom_radius_adjust.place(x=50, y=210)

    buttonback = Button(root, text="Sair", bg="red", command=root.destroy)
    buttonback.place(x=50, y=230)


    root.grab_set()
    root.wait_window()


# Função para capturar eventos do mouse (botão direito clicado)
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_RBUTTONDOWN:  # Se o botão direito for pressionado
        global x_gui, y_gui
        x_gui, y_gui = x, y
        zoom_label(x, y, current_zoom_level)  # Abre a interface de zoom
    print(current_zoom_level)

#função para salvar dados das coordenadas
# Função para salvar as coordenadas em um arquivo
def get_data(adjusted_x, adjusted_y_print, time):
    with open(f'data.txt', 'a') as file:
        file.write(f'{adjusted_x}, {adjusted_y_print}, {time}\n')

# Função para escrever coordenadas e textos na imagem (desenhar textos dinâmicos)
def image_writing(x,string, im, pos, colour):
    """
        Adiciona textos sobre a imagem mostrando informações dinâmicas como coordenadas e tempo.
        Parâmetros:
            - x: valor a ser exibido (coordenadas ou tempo)
            - string: rótulo para identificar o valor exibido
            - im: imagem de fundo onde o texto será inserido
            - pos: posição onde o texto será colocado na imagem
            - colour: cor do texto (formato BGR)
        """
    position_text = string + f'{x}'
    cv2.putText(im, position_text, pos, cv2.FONT_HERSHEY_DUPLEX, 1,colour, 2, cv2.LINE_AA)

def process_image(path):
    """
        Ajusta o tamanho da imagem de acordo com as dimensões do monitor, mantendo a proporção original.
    """
    im_defined = Image(path=path, width=0, height=0, blur=(0, 0), radius=80)  # recebimento dos parâmetros
    im_defined.height, im_defined.width, _ = im_defined.get_image_dimension()  # largura e altura imagem
    # print(str(im_defined.width), str(im_defined.height))
    im_proportion = im_defined.height / im_defined.width  # proporção altura/largura da imagem

    screen_width, screen_height = screen_info()  # largura e altura monitor
    screen_proportion = screen_height / screen_width  # proporção altura/largura monitor

    if screen_proportion > im_proportion:  # condição para imagens mais largas que o monitor
        im_defined.width = screen_width
        im_defined.height = int(im_proportion * im_defined.width)

    elif screen_proportion < im_proportion:  # condições para imagens mais altas que o monitor
        im_defined.height = screen_height
        im_defined.width = int(im_defined.height / im_proportion)

    else:  # condição para casamento de monitor e imagem
        im_defined.height, im_defined.width = screen_height, screen_width

    return im_defined, screen_width, screen_height
def start_image_viewing(path):  # função para visualização da imagem

    """
        Carrega e processa a imagem, aplicando opacidade, zoom e interação com o mouse.
    """

    im_defined, screen_width, screen_height = process_image(path)  # Processa imagem e ajusta ao tamanho do monitor
    cv2.namedWindow('imagem borrada', cv2.WND_PROP_FULLSCREEN)  # Cria uma janela em tela cheia
    cv2.setWindowProperty('imagem borrada', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Define o nível de opacidade e calcula o deslocamento da imagem na tela
    im_defined.blur = (30, 30)  # Aplica desfoque (opacidade)
    x_offset = (screen_width - im_defined.width) // 2
    y_offset = (screen_height - im_defined.height) // 2

    # Carrega a imagem original e a versão desfocada
    blur_image = im_defined.resize_image()
    def_im = cv2.imread(im_defined.path)
    def_im = cv2.resize(def_im, (im_defined.width, im_defined.height))

    # Inicializa o arquivo onde os dados de coordenadas serão armazenados
    with open('data.txt', 'w') as f:
        f.write('X,Y,T\n')  # Cabeçalho do arquivo

    # Buffers para armazenar coordenadas temporariamente
    buffer_x = []
    buffer_y = []
    buffer_time = []
    k = 0  # Contador de coordenadas salvas
    start_time = time.time()  # Inicia a contagem do tempo
    # Restante do código principal
    while True:

        print(f'{flag_change_radius=}')

        cv2.setMouseCallback('imagem borrada', mouse_callback)
        if current_zoom_level==1:
            x_correction = 0
            y_correction = 0

        x, y = mouse_position()

        adjusted_x = int((x - x_correction - x_gui)/current_zoom_level +x_gui - x_offset)
        adjusted_y = int((y + y_correction - y_gui)/current_zoom_level + y_gui -y_offset)
        adjusted_y_print = int(screen_height - y - y_correction)

        mask = np.zeros(def_im.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (adjusted_x, adjusted_y),im_def.radius, 255, -1)
        print(f'Esse é o zoom na lupa {im_defined.radius=}')
        #print(f'Posição lupa: x= {adjusted_x}, y= {adjusted_y_print}')
        mask_inv = cv2.bitwise_not(mask)
        masked_blur = cv2.bitwise_and(blur_image, blur_image, mask=mask_inv)
        masked_orig = cv2.bitwise_and(def_im, def_im, mask=mask)

        combined_image = cv2.add(masked_blur, masked_orig)

        background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
        background[y_offset:y_offset + im_defined.height, x_offset:x_offset + im_defined.width] = combined_image
        cv2.circle(background, (adjusted_x + x_offset, adjusted_y + y_offset), im_def.radius, 255, 10)
        #ver limites do offset

        # Aplique o nível de zoom atual
        if current_zoom_level != 1:
            background, adjusted_x, adjusted_y_print, x_correction, y_correction, lim_x, lim_y  = centering(background, x_gui,y_gui,current_zoom_level, x_offset, y_offset)
            #background = zoom(background, current_zoom_level)
            print(f'X_offset = {x_offset}, Y_offset = {y_offset}')
        #if 0 <= adjusted_x < im_defined.width and 0 <= adjusted_y_print < im_defined.height:  # condição para o plot das coordenadas x,y
            # print("X coordenada:"+str(adjusted_x)+"Y coordenada:"+str(adjusted_y_print))
        threadx = threading.Thread(target=image_writing(adjusted_x,f'X: ', background, (10,30), (0,0,255)))
        thready = threading.Thread(target=image_writing(adjusted_y_print,f'Y: ', background, (130,30), (0,0,255)))
        threadx.start()
        thready.start()


        threadzoom = threading.Thread(target=image_writing(current_zoom_level, f'Zoom level: ', background, (10,60),(0,255,0)))
        threadzoom.start()



        if 0 <= adjusted_x < im_defined.width and 0 <= adjusted_y_print < im_defined.height:  # condição para o plot das coordenadas x,y
            print(f'{k=}')
            if k<=100:
                buffer_x.append(adjusted_x)
                buffer_y.append(adjusted_y_print)
                time_reg = time.time()-start_time

                thread_time = threading.Thread(
                    target=image_writing(int(time_reg), f'Time: ', background, (10, 90), (255, 0, 0)))
                thread_time.start()
                buffer_time.append(time_reg)
                k+=1
                thread_time.join()

            if k>100:
                print(buffer_time)
                thread = threading.Thread(target=get_data(buffer_x,buffer_y, buffer_time))
                thread.start()
                buffer_x=[]
                buffer_y=[]
                buffer_time=[]
                k=0
                thread.join()
        cv2.imshow('imagem borrada', background)
        threadx.join()
        thready.join()
        threadzoom.join()
        '''
        end = pc()

        print('tempo de proc:', str(end - start))
        '''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
