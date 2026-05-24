# IMPORTANDO AS FUNÇÕES DO SCRIPT DE TRATAMENTO
from funcoes import fazer_analise_inicial, processar_produtos, processar_pedidos

def executar_pipeline():
    print("Pipeline de tratamento iniciado")

    # Análise inicial exploratória
    fazer_analise_inicial()
    print("\nIniciando processamento e limpeza dos dados...")

    # Processamento da base de Produtos
    total_produtos, nulos_produtos = processar_produtos(
        'olist_products_dataset.csv',
        'olist_products_dataset_tratado.csv'
    )

    # Processamento da base de Pedidos
    total_pedidos, cancelados, nulas_provadas, entregas_nulas = processar_pedidos(
        'olist_orders_dataset.csv',
        'olist_orders_dataset_tratado.csv'
    )

    # Relatório final
    print("\n[RELATÓRIO FINAL]\n")

    print(f"[PRODUTOS] Linhas processadas: {total_produtos}")
    print(f"[PRODUTOS] Nulos corrigidos: {nulos_produtos}")
    print(f"[PEDIDOS] Linhas processadas: {total_pedidos}")
    print(f"[PEDIDOS] Pedidos cancelados: {cancelados}")

    print("\n[ANÁLISE DE NEGÓCIO]")

    if entregas_nulas > 0:
        percentual = (nulas_provadas / entregas_nulas) * 100
        print(
            f"{nulas_provadas} de {entregas_nulas} pedidos sem entrega são cancelados "
            f"({percentual:.2f}%)."
        )
    else:
        print("Não há pedidos com entrega nula para análise.")

    print("\nArquivos tratados e salvos com sucesso!")


if __name__ == "__main__":
    executar_pipeline()
    
