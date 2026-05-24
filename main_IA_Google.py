from funcoes_IA_Google import tratar_produtos, tratar_pedidos

# 1. Execução do pipeline para Produtos
produtos_sanitizados, nulos_categoria = tratar_produtos("olist_products_dataset.csv")

# 2. Execução do pipeline para Pedidos
pedidos_sanitizados, entregas_nulas, cancelados, validacao_hipotese = tratar_pedidos("olist_orders_dataset.csv")

# 3. Exibição do Relatório de Status Manual (Sumário Estatístico)
print("=" * 10 + " RELATÓRIO DE SANITIZAÇÃO (ETL) " + "=" * 10)
print(f"Total de produtos finais processados/válidos: {len(produtos_sanitizados)}")
print(f"Total de categorias ausentes corrigidas:      {nulos_categoria}")
print("-" * 52)
print(f"Total de registros de pedidos analisados:     {len(pedidos_sanitizados)}")
print(f"Total de pedidos cancelados identificados:    {cancelados}")
print(f"Total de pedidos com data de entrega nula:    {entregas_nulas}")
print("-" * 52)

print("ANÁLISE DA HIPÓTESE DE NEGÓCIO:")
if validacao_hipotese:
    print("-> HIPÓTESE CONFIRMADA: Todas as datas de entrega nulas devem-se estritamente a pedidos cancelados.")
else:
    print("-> HIPÓTESE REJEITADA: Existem datas de entrega nulas em pedidos cujo status não é 'canceled'.")
    print("   (Pedidos podem estar atrasados, faturados ou em rota de transporte comercial).")
print("=" * 52)
