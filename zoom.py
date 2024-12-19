# Made by Felipe Meier Martins
# Collab PET EEL - LPDS
# ----------------------------------------------------------

# zoom.py
import cv2  # Biblioteca OpenCV para manipulação de imagens
from mouse_manipulator import mouse_position  # Função externa que captura a posição do mouse
import numpy as np  # Biblioteca NumPy para cálculos numéricos eficientes

def centering(in_image, x_click=0, y_click=0, zoom=0, x_og_offset=0, y_og_offset=0):
    '''
    Função responsável por centralizar o ponto de interesse na imagem
    e aplicar zoom na região selecionada pelo usuário.

    Parâmetros:
    - in_image: imagem original a ser processada.
    - x_click: coordenada x do clique do usuário.
    - y_click: coordenada y do clique do usuário.
    - zoom: nível de zoom a ser aplicado.
    - x_og_offset: deslocamento original no eixo x.
    - y_og_offset: deslocamento original no eixo y.
    '''

    # Obtém as dimensões da imagem: altura, largura e canais de cor
    in_height, in_width, _ = in_image.shape
    x_med, y_med = int(in_width / 2), int(in_height / 2)  # Calcula o centro da imagem original

    # Ajusta a coordenada y para que a origem (0,0) seja no canto inferior esquerdo
    y_click = in_height - y_click
    y_med = in_height - y_med

    # Calcula a diferença entre o centro da imagem e o ponto clicado pelo usuário
    x_borda = x_med - x_click
    y_borda = y_med - y_click

    # Inicializa as bordas que serão usadas para "preencher" as áreas fora da imagem
    top_border, bottom_border, right_border, left_border = 0, 0, 0, 0

    # Ajuste da borda no eixo x
    if x_borda > 0:  # Se o ponto de interesse estiver à esquerda do centro
        left_border = x_borda  # Preenche a borda esquerda
        x_offset = x_borda  # Deslocamento no eixo x
    else:  # Se o ponto estiver à direita do centro
        right_border = -x_borda  # Preenche a borda direita
        x_offset = x_borda  # Deslocamento no eixo x

    # Ajuste da borda no eixo y
    if y_borda > 0:  # Se o ponto estiver acima do centro
        bottom_border = y_borda  # Preenche a borda inferior
        y_offset = y_borda  # Deslocamento no eixo y
    else:  # Se o ponto estiver abaixo do centro
        top_border = -y_borda  # Preenche a borda superior
        y_offset = y_borda  # Deslocamento no eixo y

    # Recorta a região da imagem centralizada no ponto de interesse
    center_image = in_image[bottom_border:in_height-top_border, right_border:in_width-left_border]

    # Adiciona bordas pretas para manter a imagem centralizada na tela
    center_image = cv2.copyMakeBorder(center_image, top_border, bottom_border,
                                      left_border, right_border, cv2.BORDER_CONSTANT, value=[255, 0, 0])

    # Calcula os limites para aplicar o zoom na imagem centralizada
    xin = x_med - x_med / zoom  # Limite esquerdo
    xend = x_med + x_med / zoom  # Limite direito
    yin = y_med - y_med / zoom  # Limite superior
    yend = y_med + y_med / zoom  # Limite inferior

    # Recorta a região correspondente ao zoom
    center_image = center_image[int(yin):int(yend), int(xin):int(xend)]

    # Redimensiona a imagem de volta ao tamanho original, aplicando o zoom com interpolação
    center_image = cv2.resize(center_image, (in_width, in_height), interpolation=cv2.INTER_CUBIC)

    # Ajuste das coordenadas do clique em relação aos deslocamentos originais
    x_click_adp = x_click - x_og_offset
    y_click_adp = y_click - y_og_offset

    # Imprime valores de debug (úteis para checar os cálculos intermediários)
    print(f'{xin=}, {xend=}, {yin=}, {yend=}, {x_click}, {y_click}')
    print(f'{xin=}, {xend=},{yin=}, {yend=}. {x_med=}, {y_med=}. {x_click_adp=},{y_click_adp=} {y_click=}, {x_click=},{y_click=}, {x_borda= }, {y_borda= }')

    # Captura a posição atual do mouse
    x_mouse, y_mouse = mouse_position()
    y_mouse = in_height - y_mouse  # Ajusta a coordenada y do mouse para começar do canto inferior

    # Ajusta a posição do mouse em relação ao zoom e deslocamentos
    adjusted_x = int((x_mouse) / zoom + x_click - x_og_offset - (x_med / zoom))
    adjusted_y = int((y_mouse) / zoom + y_click - y_og_offset - (y_med / zoom))

    # Retorna a imagem centralizada, as coordenadas ajustadas e deslocamentos
    return center_image, adjusted_x, adjusted_y, x_offset, y_offset, xin, yin
