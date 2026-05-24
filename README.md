## Mini-Projeto-Avaliativo---M1S07-SCTEC
**Mini-Projeto avaliativo do curso Machine Learning e Visão Computacional SCTEC**

## Pipeline de ETL – Tratamento de Dados Olist

## Visão Geral
Este projeto implementa um pipeline de ETL (Extract, Transform, Load) para tratamento de dados da base pública da Olist, com foco em garantir qualidade, consistência e padronização das informações para uso analítico e em modelos de Machine Learning.


## Objetivo
Preparar os dados para consumo confiável, reduzindo problemas como:
- valores nulos  
- inconsistências  
- ruído estatístico  
- viés em modelos preditivos  


## Etapas do Pipeline
**Análise Inicial**
- Leitura dos arquivos CSV  
- Inspeção de colunas e estrutura  

**Tratamento de Produtos**
- Padronização de categorias  
- Remoção de caracteres especiais  
- Tratamento de valores nulos  
- Imputação com mediana em variáveis numéricas  

**Tratamento de Pedidos**
- Identificação de pedidos cancelados  
- Análise de entregas não realizadas  
- Padronização de datas  
- Consolidação de indicadores  

**Geração de Saída**
- Criação de arquivos tratados  
- Exibição de relatório com métricas do processamento  

## Estratégia de Tratamento de Dados
Para valores numéricos ausentes, foi utilizada a **mediana** como técnica de imputação.
Essa abordagem foi adotada por:
- ser resistente a valores extremos (outliers)  
- preservar melhor a distribuição dos dados  
- evitar distorções que impactam modelos de Machine Learning  
- seguir boas práticas de engenharia de dados  

## Tecnologias Utilizadas
- Python  
- Bibliotecas nativas:
  - csv  
  - re  
  - datetime  

## Execução
python main.py


Autor: Zegmundo Koziel Junior
Linkedin: https://www.linkedin.com/in/zegmundo-koziel/
GitHub: https://github.com/zegmundo-koziel
