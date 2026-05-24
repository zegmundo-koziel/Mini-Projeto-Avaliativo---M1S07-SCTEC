# IMPORTANDO AS BIBLIOTECAS NATIVAS
import csv
import re
from datetime import datetime

# Variável global com os nomes dos arquivos brutos
arquivos = ['olist_orders_dataset.csv', 'olist_products_dataset.csv']


# ANÁLISE INICIAL DOS DADOS
def fazer_analise_inicial():
    """Mostra as colunas e a primeira linha de dados de cada arquivo para análise."""
    for nome_arquivo in arquivos:
        print(f"\n###### LENDO ARQUIVO: {nome_arquivo} ######")
        try:
            with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo:
                leitor = csv.reader(arquivo)
                colunas = next(leitor)
                primeira_linha = next(leitor)

                print("COLUNAS -----> PRIMEIRO DADO")
                for col, dado in zip(colunas, primeira_linha):
                    print(f"• {col} ----- {dado}")

        except FileNotFoundError:
            print(f"ERRO: O arquivo '{nome_arquivo}' não foi encontrado.")


# FUNÇÕES DE SUPORTE
def limpar_nome_categoria(nome):
    """Padroniza nomes de categorias."""
    if not nome or nome.strip() == "":
        return "sem categoria"

    nome_limpo = nome.lower().strip()
    nome_limpo = re.sub(r'[^\w\s]', '', nome_limpo)
    return nome_limpo


# A mediana foi escolhida porque: reduz o impacto de valores extremos; mantém integridade estatística
# evita distorção da base, melhora a qualidade para modelos futuros
def calcular_mediana(arquivo_original, colunas_alvo):
    """Calcula mediana das colunas numéricas."""
    valores_por_coluna = {col: [] for col in colunas_alvo}

    with open(arquivo_original, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            for col in colunas_alvo:
                valor = linha[col].strip()
                if valor:
                    try:
                        valores_por_coluna[col].append(float(valor))
                    except ValueError:
                        continue

    medianas = {}
    for col, lista in valores_por_coluna.items():
        if not lista:
            medianas[col] = 0.0
            continue

        lista.sort()
        n = len(lista)
        meio = n // 2

        if n % 2 == 0:
            medianas[col] = (lista[meio - 1] + lista[meio]) / 2
        else:
            medianas[col] = lista[meio]

    return medianas


# PROCESSAMENTO DE PRODUTOS
def processar_produtos(arquivo_original, arquivo_destino):
    dimensoes = [
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]

    medianas = calcular_mediana(arquivo_original, dimensoes)

    produtos_tratados = []
    contador_nulos_corrigidos = 0

    with open(arquivo_original, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        cabecalhos = leitor.fieldnames

        for linha in leitor:
            # Categoria
            categoria_original = linha['product_category_name']
            categoria_tratada = limpar_nome_categoria(categoria_original)

            if not categoria_original or categoria_original.strip() == "":
                contador_nulos_corrigidos += 1

            linha['product_category_name'] = categoria_tratada

            # Dimensões
            for col in dimensoes:
                valor = linha[col].strip()

                if not valor:
                    linha[col] = float(medianas[col])
                    contador_nulos_corrigidos += 1
                else:
                    linha[col] = float(valor)

            produtos_tratados.append(linha)

    with open(arquivo_destino, mode='w', encoding='utf-8', newline='') as saida:
        escritor = csv.DictWriter(saida, fieldnames=cabecalhos)
        escritor.writeheader()
        escritor.writerows(produtos_tratados)

    return len(produtos_tratados), contador_nulos_corrigidos


# PROCESSAMENTO DE PEDIDOS
def processar_pedidos(arquivo_original, arquivo_destino):
    pedidos_tratados = []

    total_linhas = 0
    pedidos_cancelados = 0
    entregas_nulas = 0
    nulas_provadas = 0

    with open(arquivo_original, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        cabecalhos = leitor.fieldnames

        for linha in leitor:
            total_linhas += 1

            status = linha['order_status'].strip()
            data_entrega = linha['order_delivered_customer_date'].strip()
            data_aprovacao = linha['order_approved_at'].strip()

            if status == 'canceled':
                pedidos_cancelados += 1

            # Contagem de entregas nulas
            if not data_entrega:
                entregas_nulas += 1

                if status == 'canceled':
                    nulas_provadas += 1

            # Conversão de data
            if data_aprovacao:
                try:
                    dt = datetime.strptime(data_aprovacao, "%Y-%m-%d %H:%M:%S")
                    linha['order_approved_at'] = dt.strftime("%d/%m/%Y")
                except ValueError:
                    pass

            pedidos_tratados.append(linha)

    with open(arquivo_destino, mode='w', encoding='utf-8', newline='') as saida:
        escritor = csv.DictWriter(saida, fieldnames=cabecalhos)
        escritor.writeheader()
        escritor.writerows(pedidos_tratados)

    return total_linhas, pedidos_cancelados, nulas_provadas, entregas_nulas
