# Made by Felipe Meier Martins
# Collab PET EEL - LPDS
# ----------------------------------------------------------

# Importa bibliotecas necessárias
import pandas as pd  # Biblioteca para manipulação e análise de dados
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos
import seaborn as sns  # Biblioteca para visualização de dados avançada
import ast  # Biblioteca para avaliar strings como estruturas de dados Python
import os  # Biblioteca para manipulação de diretórios e arquivos


# Função principal para processar os dados
def proc_data(width, height, radius):
    """
    Processa os dados de movimento do mouse a partir de um arquivo de texto,
    calcula a frequência em cada coordenada (X, Y) e gera um heatmap (mapa de calor).

    Parâmetros:
        - width: Largura da imagem (incrementada durante o processamento)
        - height: Altura da imagem (incrementada durante o processamento)
        - radius: Raio da lupa (não utilizado diretamente nesta função)
    """
    # Incrementa as dimensões da imagem (adiciona 1 a altura e largura)
    width += 1
    height += 1

    # Define o caminho do arquivo de entrada
    file_path = 'data.txt'

    # Listas para armazenar os valores de X (coordenadas), Y (coordenadas) e T (tempo)
    X_vals, Y_vals, T_vals = [], [], []

    # Abre o arquivo 'data.txt' para leitura
    with open(file_path, 'r') as file:
        file.readline()  # Ignora a primeira linha do arquivo (cabeçalho)
        for line in file:
            if line.strip():  # Verifica se a linha não está vazia
                # Divide os valores da linha nos blocos de coordenadas
                vectors = line.strip().split('], [')

                # Converte os valores da string para listas de números usando ast.literal_eval
                X = list(map(float, ast.literal_eval(vectors[0].replace('[', '').replace(']', ''))))
                Y = list(map(float, ast.literal_eval(vectors[1].replace('[', '').replace(']', ''))))
                T = list(map(float, ast.literal_eval(vectors[2].replace('[', '').replace(']', ''))))

                # Adiciona os valores extraídos às listas principais
                X_vals.extend(X)
                Y_vals.extend(Y)
                T_vals.extend(T)

    # Cria um DataFrame (tabela) com as colunas X, Y e T (tempo)
    df = pd.DataFrame({'X': X_vals, 'Y': Y_vals, 'T': T_vals})

    # Agrupa os dados por coordenadas (X, Y) e conta a frequência de cada ponto
    df_counts = df.groupby(['X', 'Y']).size().reset_index(name='Count')

    # Cria todas as coordenadas possíveis em uma grade (baseado em largura e altura)
    all_coords = pd.MultiIndex.from_product([range(width), range(height)], names=['X', 'Y']).to_frame(index=False)

    # Faz um "merge" com todas as coordenadas possíveis e os dados reais
    # Preenche os valores ausentes com 0 (se uma coordenada não tiver dados, a contagem será zero)
    df_full = pd.merge(all_coords, df_counts, on=['X', 'Y'], how='left').fillna(0)

    # Garante que a coluna 'Count' seja do tipo inteiro
    df_full['Count'] = df_full['Count'].astype(int)

    # Soma total dos valores da coluna 'Count'
    count_total = df_full['Count'].sum()
    print(f"Total de Count: {count_total}")

    # Converte os valores de 'Count' para porcentagem, caso o total seja maior que zero
    if count_total > 0:
        df_full['Count'] = df_full['Count'] / count_total * 100
    else:
        # Caso não existam dados válidos, exibe um erro e encerra a função
        print("Erro: Total de Count é zero. Verifique os dados de entrada.")
        return

    # Cria uma matriz para o heatmap, onde as linhas são 'Y' e as colunas são 'X'
    heatmap_data = df_full.pivot(index='Y', columns='X', values='Count')

    # Exibe no console a matriz de dados do heatmap (para depuração)
    print(f"Ese é o {heatmap_data= }")

    # Cria o heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, cmap='viridis', cbar_kws={'label': 'Frequência (%)'})
    plt.title('Heatmap de Movimento do Mouse')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')

    # Inverter o eixo Y para que a origem fique no canto inferior esquerdo
    plt.gca().invert_yaxis()

    # Salva o heatmap como uma imagem
    output_dir = os.path.join(os.getcwd(), "Imagens")
    os.makedirs(output_dir, exist_ok=True)  # Cria o diretório se não existir
    output_path = os.path.join(output_dir, "heatmap.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Heatmap salvo em: {output_path}")

    # Salva o DataFrame original (X, Y, T) em um arquivo CSV para análise futura
    df.to_csv('dados.csv', sep=',', index=False)
