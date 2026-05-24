import csv
import re
from datetime import datetime

# Variável global com os nomes dos arquivos brutos
arquivos = ['olist_orders_dataset.csv', 'olist_products_dataset.csv']

def limpar_categoria(categoria):
    """
    Sprint: Padronização de Strings e Regex
    Converte para minúsculas, limpa espaços nas bordas e remove caracteres especiais.
    """
    if not categoria or categoria.strip() == "":
        return "sem categoria"
    
    categoria = categoria.lower().strip()
    # Mantém letras minúsculas (a-z), números (0-9), underlines (_) e espaços ( )
    categoria = re.sub(r'[^a-z0-9_ ]', '', categoria)
    return categoria


def tratar_produtos(arquivo):
    """
    Sprint: Validação e Tratamento de Dados Ausentes
    Lê a base de produtos aplicando as regras de tratamento de nulos.
    """
    dados = []
    nulos_categoria_corrigidos = 0

    with open(arquivo, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for linha in reader:
            # 1. Tratamento da Categoria Ausente
            if not linha.get('product_category_name') or linha['product_category_name'].strip() == "":
                linha['product_category_name'] = "Sem Categoria"
                nulos_categoria_corrigidos += 1
            else:
                linha['product_category_name'] = limpar_categoria(linha['product_category_name'])

            # 2. Regra de corte para dimensões físicas:
            # TÉCNICA ESCOLHIDA: Descarte (Regra de corte por deleção).
            # JUSTIFICATIVA: Produtos sem peso ou dimensões físicas não podem ter fretes calculados 
            # corretamente pela infraestrutura logística, sendo preferível removê-los do pipeline 
            # para evitar que alimentem modelos preditivos com dados corrompidos ou inconsistentes.
            if not linha.get('product_weight_g') or not linha.get('product_length_cm'):
                continue  # Ignora e descarta o registro inconsistente

            dados.append(linha)

    return dados, nulos_categoria_corrigidos


def tratar_pedidos(arquivo):
    """
    Sprints: Lógica de Regra de Negócio & Formatação Temporal
    Avalia a correlação de datas de entrega vazias e converte datas válidas.
    """
    dados_pedidos = []
    pedidos_cancelados = 0
    datas_entrega_nulas = 0
    comprova_hipotese_estrita = 0  # Conta se nulo ocorre APENAS por cancelamento

    with open(arquivo, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for linha in reader:
            status = linha.get('order_status')
            data_entrega = linha.get('order_delivered_customer_date')
            data_aprovacao = linha.get('order_approved_at')

            # 1. Avaliação de Regra de Negócio (Hipótese das datas de entrega vazias)
            if not data_entrega or data_entrega.strip() == "":
                datas_entrega_nulas += 1
                if status == 'canceled':
                    comprova_hipotese_estrita += 1

            if status == 'canceled':
                pedidos_cancelados += 1

            # 2. Formatação Temporal (Datetime)
            if data_aprovacao and data_aprovacao.strip() != "":
                try:
                    # Converte a string original para objeto datetime
                    dt = datetime.strptime(data_aprovacao, "%Y-%m-%d %H:%M:%S")
                    # Formata o objeto para o padrão brasileiro simplificado
                    linha['order_approved_at_ptbr'] = dt.strftime("%d/%m/%Y")
                except ValueError:
                    linha['order_approved_at_ptbr'] = "Data Inválida"
            else:
                linha['order_approved_at_ptbr'] = "Não Aprovado"

            dados_pedidos.append(linha)

    # Verifica se a hipótese da diretoria está 100% correta
    # (Se todas as datas nulas forem decorrentes de cancelamento)
    hipotese_confirmada = (datas_entrega_nulas == comprova_hipotese_estrita)

    return dados_pedidos, datas_entrega_nulas, pedidos_cancelados, hipotese_confirmada
