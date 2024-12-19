# Made by Felipe Meier Martins
# Collab PET EEL - LPDS
# ----------------------------------------------------------
'''
Arquivo principal da aplicação. Este script orquestra o funcionamento do programa,
chamando os módulos responsáveis pela interface gráfica, processamento de imagem,
prioridade do sistema e manipulação de dados.
'''

from toolbar import menu  # Importa a função do menu principal
from image_manipulator import start_image_viewing, process_image  # Importa funções para processamento de imagem
import cv2  # OpenCV para manipulação de imagens
import os  # Biblioteca para operações de sistema, como manipulação de arquivos
from data import proc_data  # Função para processar dados relacionados à imagem
from priority_task import set_priority  # Função para definir a prioridade do programa no sistema

# Define o programa como prioridade em tempo real no sistema operacional
set_priority("tempo_real")  # Torna o programa mais responsivo ao priorizar suas tarefas

# Variável global que armazena o nível de zoom atual
current_zoom_level = 1

# Exibe o menu principal e permite ao usuário interagir com a interface gráfica
monitor = menu()

# Verifica se o estado da aplicação (flag_start) indica que a visualização foi iniciada
if monitor.get_flag_start() == 1:
    # Inicia a visualização da imagem selecionada no menu
    start_image_viewing(monitor.path)

# Verifica se o estado da aplicação (flag_start) indica que o programa deve ser encerrado
if monitor.get_flag_start() == 2:
    # Fecha todas as janelas abertas pelo OpenCV
    cv2.destroyAllWindows()
    #quit()  # Encerra o programa completamente (sem mostrar o histograma)
else:
    # Caso nenhum dos estados acima ocorra, informa que a visualização não foi iniciada
    print("Visualização não iniciada")

# Processa a imagem selecionada para obter suas dimensões e outros parâmetros
im_defined, _, _ = process_image(path=monitor.path)  # Retorna a imagem processada e suas dimensões
im_height = im_defined.height  # Armazena a altura da imagem
im_width = im_defined.width  # Armazena a largura da imagem

# Processa os dados da imagem, passando largura, altura e raio da lupa focal
proc_data(im_width, im_height, im_defined.radius)

# Caminho do arquivo de dados a ser manipulado
caminho_arquivo = r'data.txt'

# Verifica se o arquivo de dados existe antes de tentar apagá-lo
if os.path.exists(caminho_arquivo):
    # Apaga o arquivo existente para limpar os dados antigos
    os.remove(caminho_arquivo)
    print(f'Arquivo {caminho_arquivo} apagado com sucesso.')  # Confirma que o arquivo foi apagado
else:
    # Caso o arquivo não exista, exibe uma mensagem informando
    print(f'Arquivo {caminho_arquivo} não encontrado.')
