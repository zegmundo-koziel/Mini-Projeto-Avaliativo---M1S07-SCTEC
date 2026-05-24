MODOLO GERADO POR IA - GEMINI 

# Pipeline de Sanitização de Dados - E-commerce Olist

Este repositório contém a solução do Mini-Projeto Avaliativo (Módulo 1 - Semana 07) do curso de Machine Learning e Visão Computacional. O objetivo é construir um pipeline estruturado de extração e transformação (ETL) utilizando apenas recursos nativos do Python.

## 🛠️ Tecnologias Utilizadas
* **Python 3** (Bibliotecas nativas: `csv`, `re`, `datetime`).

## 📋 Como Executar o Projeto
1. Certifique-se de que os arquivos `olist_products_dataset.csv` e `olist_orders_dataset.csv` estão na mesma pasta que os scripts.
2. Execute o arquivo principal via terminal:
```bash
python main_AI_Google.py
```

## 🧠 Reflexão Teórica: Evitando o Overfitting e Viés através do ETL

No ciclo de desenvolvimento de uma Inteligência Artificial, a qualidade da base de dados fornecida à fase de treinamento dita o teto de acertos do modelo preditivo. Dados brutos inconsistentes, contendo strings mal-formatadas ou campos nulos desordenados, propagam ruídos matemáticos. Se um algoritmo de aprendizado supervisionado mapear registros corrompidos, ele poderá sofrer de **Overfitting**, decorando imperfeições temporárias e anomalias logísticas da base de dados em vez de aprender padrões estatísticos reais. Consequentemente, o modelo terá um desempenho excelente nos testes internos, mas falhará em dados de produção no mundo real.

A aplicação de regras rígidas de corte, sanitização de strings via Expressões Regulares (Regex) e a substituição lógica de valores ausentes estabelecem uma infraestrutura confiável. Essa consistência blinda o modelo contra **vieses indesejados** (como classificar erroneamente categorias devido a variações de grafia e maiúsculas) e impede o colapso de tensores analíticos na entrada da rede neural. Garantir o tratamento correto na camada de engenharia nativa cumpre a máxima de que uma IA sólida depende diretamente de dados limpos.
