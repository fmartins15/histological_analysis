# Made by Felipe Meier Martins
# Collab PET EEL - LPDS
# ----------------------------------------------------------
'''
Esse arquivo é responsável pelo menu principal e pelas GUIs (Interfaces Gráficas)
para seleção de imagens, além da exibição do manual de instruções.
'''

from tkinter import *  # Importa a biblioteca Tkinter para criação de interfaces gráficas
from PIL import Image as PilImage, ImageTk  # Pillow é usado para carregar e manipular imagens
from image_manipulator import start_image_viewing, screen_info  # Importa funções auxiliares
import os  # Biblioteca para manipulação de diretórios e arquivos

# Classe principal que cria a interface gráfica (GUI)
class Example(Frame):

    # Método inicializador da classe
    def __init__(self, command, path, flag_start):
        self.path = path  # Caminho inicial da imagem (vazio por padrão)
        self.command = command  # Comando associado ao processamento de imagem
        self.flag_start = 0  # Variável que indica o estado do programa
        super().__init__()  # Inicializa a classe pai Frame

        self.initUI()  # Chama a função que inicializa a interface gráfica

    # Método que cria uma janela para seleção de imagens
    def choose_image(self):
        # Cria uma nova janela para escolha de imagem
        im_root = Toplevel(self)
        im_root.title("Escolha uma Imagem")  # Título da janela
        im_root.geometry("400x300")  # Define o tamanho da janela

        # Define o diretório onde as imagens estão armazenadas
        pasta = r'C:\Users\meier\Downloads\lpdsproject\Imagens'
        list_images = [vv for vv in os.listdir(pasta)]  # Lista todas as imagens no diretório
        print(list_images)  # Imprime a lista de imagens no console

        # Cria um widget Listbox para exibir a lista de imagens
        listbox = Listbox(im_root)
        listbox.pack(fill='both', expand=True)  # Expande o Listbox para preencher a janela

        # Preenche a Listbox com os nomes das imagens
        for img in list_images:
            listbox.insert('end', img)

        # Função que obtém o caminho da imagem selecionada
        def get_selected_image_path(event):
            selected_index = listbox.curselection()  # Captura a imagem selecionada
            if selected_index:
                selected_image = list_images[selected_index[0]]  # Obtém o nome da imagem
                image_path = os.path.join(pasta, selected_image)  # Monta o caminho completo
                print(f"Caminho da imagem selecionada: {image_path}")
                self.flag_start = 1  # Atualiza o estado
                self.path = image_path  # Armazena o caminho da imagem
                start_image_viewing(image_path)  # Chama a função para visualizar a imagem
                im_root.destroy()  # Fecha a janela após a escolha

        # Associa o evento de seleção na Listbox à função acima
        listbox.bind('<<ListboxSelect>>', get_selected_image_path)

    # Método para abrir o manual de instruções em uma nova janela
    def open_instructions(self, label, txtfile):
        instructions_window = Toplevel()  # Cria uma nova janela
        instructions_window.title(label)
        instructions_window.geometry("400x300")  # Define o tamanho da janela

        # Caminho para o arquivo de texto com as instruções
        instructions_path = os.path.join(label, txtfile)

        # Abre e lê o arquivo de texto com as instruções
        with open(instructions_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Cria um widget Text para exibir o conteúdo
        text_widget = Text(instructions_window, wrap='word')  # Quebra linhas automaticamente
        text_widget.insert('1.0', content)  # Insere o conteúdo no widget
        text_widget.pack(expand=True, fill='both')  # Expande o widget para preencher a janela
        text_widget.config(state=DISABLED)  # Impede a edição do texto

    # Método que inicializa a interface gráfica (barra de menus)
    def initUI(self):
        self.master.title("Menu inicial")  # Define o título da janela principal

        menubar = Menu(self.master)  # Cria uma barra de menus
        self.master.config(menu=menubar)  # Associa a barra de menus à janela principal

        file_menu = Menu(menubar)  # Cria um menu chamado "Arquivo"
        file_menu.add_command(label="Escolher imagem", command=self.choose_image)  # Opção de escolher imagem
        file_menu.add_command(label="Salvar")  # (Futuro recurso: salvar imagem)
        file_menu.add_separator()  # Adiciona uma linha separadora
        file_menu.add_command(label="Sair", command=self.on_stop)  # Opção de sair do programa

        menubar.add_cascade(label="Arquivo", menu=file_menu)  # Adiciona o menu "Arquivo" na barra de menus

        # Cria um menu separado para as instruções
        instructions_menu = Menu(menubar, tearoff=0)
        instructions_menu.add_command(label="Como Usar o Programa", command= lambda: self.open_instructions('Instruções', r'C:\Users\meier\Downloads\lpdsproject\Instruções\instrucoes.txt'))

        # Adiciona o menu "Instruções" na barra de menus
        menubar.add_cascade(label="Instruções", menu=instructions_menu)

        # Cria um menu separado para "sobre o programa"
        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label="Como Usar o Programa", command=lambda: self.open_instructions('Sobre o Programa',
                                                                                                           r'C:\Users\meier\Downloads\lpdsproject\Instruções\about.txt'))

        # Adiciona o menu "Sobre o Programa" na barra de menus
        menubar.add_cascade(label="Sobre o Programa", menu=about_menu)

    # Método chamado ao iniciar o processamento de imagem
    def on_start_viewing(self):
        self.flag_start = 1  # Atualiza o estado
        print(self.flag_start)  # Imprime o estado no console
        self.command()  # Chama a função associada
        return self.flag_start

    # Método chamado para fechar o programa
    def on_stop(self):
        self.flag_start = 2  # Atualiza o estado
        print(self.flag_start)  # Imprime o estado no console
        self.master.quit()  # Fecha a janela principal
        return self.flag_start

    # Método que retorna o estado atual (flag_start)
    def get_flag_start(self):
        return self.flag_start

# Função principal que exibe o menu inicial
def menu():
    root = Tk()  # Cria a janela principal
    root.title("Tela de Menu")  # Define o título da janela

    root_width, root_height = screen_info()  # Obtém as dimensões do monitor
    root.geometry(f"{root_width}x{root_height}")  # Ajusta o tamanho da janela ao monitor

    # Carrega a imagem de fundo usando Pillow
    image_path = 'Imagens/menufoto.png'
    pil_image = PilImage.open(image_path)  # Abre a imagem
    screen_width, screen_height = screen_info()  # Redimensiona para o tamanho da tela
    pil_image = pil_image.resize((screen_width, screen_height), PilImage.LANCZOS)
    tk_image = ImageTk.PhotoImage(pil_image)  # Converte para formato compatível com Tkinter

    # Cria um Label para exibir a imagem de fundo
    image_label = Label(root, image=tk_image)
    image_label.pack()  # Adiciona a imagem à janela

    app = Example(command=start_image_viewing, path='', flag_start=0)  # Inicializa o menu principal
    app.pack()  # Adiciona o frame ao root

    root.mainloop()  # Inicia o loop principal da interface gráfica
    return app
