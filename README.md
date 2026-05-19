# 📊 Dashboard Superstore - ITA Jr. (Semana 6 / Aula 06)

Este projeto é um dashboard interativo desenvolvido em **Python** com **Streamlit**, construído como parte da avaliação/estudo da **ITA Jr**. Ele consome dados de vendas de uma loja (Superstore) armazenados na nuvem através do **Supabase** (PostgreSQL) e apresenta análises e visualizações de dados para responder a perguntas de negócio.

## 🚀 Funcionalidades

O dashboard possui quatro abas principais que estruturam a navegação:
1. **Visão Geral**: Apresenta KPIs principais, visualização em tabela dos dados e um **botão para download (CSV)** dos dados filtrados.
2. **Análise 1 a 5**: 
   * **Q1:** Cidade líder em 'Office Supplies'.
   * **Q2:** Evolução de Vendas ao longo do tempo (Gráfico de Barras).
   * **Q3:** Total de vendas por Estado.
   * **Q4:** Top N Cidades em vendas (parâmetro dinâmico).
   * **Q5:** Proporção de vendas por Segmento.
3. **Análise 6 a 10**: 
   * **Q6:** Vendas Anuais por Segmento.
   * **Q7 e Q8:** **Simulador Interativo** de Descontos (sliders para testar cenários de limite de valor e % de desconto).
   * **Q9:** Evolução da Média Mensal de vendas (Facetado por Ano e Segmento).
   * **Q10:** Top 12 Subcategorias mais rentáveis.
4. **Conclusões & Limitações**: Insights de negócio, recomendações estratégicas e uma seção dedicada à qualidade e **limitações dos dados**.

O **Menu Lateral (Sidebar)** possui filtros globais obrigatórios e dinâmicos: Período de Datas, Região, Segmento, Categoria e Subcategoria.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Streamlit:** Construção da interface web interativa.
* **Pandas:** Manipulação, limpeza e tratamento dos dados.
* **Plotly Express:** Criação dos gráficos interativos.
* **Supabase:** Banco de dados em nuvem (BaaS) utilizado para armazenar os dados do arquivo `Sample-Superstore.csv`.
* **Python-dotenv:** Gerenciamento seguro de variáveis de ambiente.

## 📁 Estrutura do Projeto

```text
aula06/
├── src/
│   ├── __init__.py         # Torna a pasta um módulo reconhecível pelo Python
│   └── database.py         # Script de conexão com o Supabase e tratamento de dados (ETL)
├── .env.example            # Exemplo de configuração das variáveis de ambiente (sem chaves reais)
├── app.py                  # Script principal que renderiza o dashboard no Streamlit
├── requirements.txt        # Lista de dependências e bibliotecas do projeto
└── README.md               # Documentação do projeto