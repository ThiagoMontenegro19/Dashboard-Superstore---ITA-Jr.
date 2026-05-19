import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import carregar_e_tratar_dados

# Configuração da página (Deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="Dashboard Superstore", layout="wide")

# 1. Carregar dados do banco Supabase através da src/database.py
df = carregar_e_tratar_dados()

if df.empty:
    st.warning("Aguardando dados do banco... Verifique a conexão ou o RLS no Supabase.")
else:
    # --- SIDEBAR (Filtros Interativos e Completos) ---
    st.sidebar.header("Filtros Dinâmicos")

    # Filtro de Data
    min_date = df['Order Date'].min().date()
    max_date = df['Order Date'].max().date()
    data_inicio, data_fim = st.sidebar.date_input(
        "Período de Datas", [min_date, max_date],
        min_value=min_date, max_value=max_date
    )

    # Filtro de Região
    regioes = df['Region'].unique()
    regiao_sel = st.sidebar.multiselect("Região", regioes, default=regioes)

    # Filtro de Segmento
    segmentos = df['Segment'].unique()
    segmento_sel = st.sidebar.multiselect("Segmento", segmentos, default=segmentos)

    # Filtro de Categoria e Subcategoria
    categorias = df['Category'].unique()
    cat_sel = st.sidebar.multiselect("Categoria", categorias, default=categorias)

    # Subcategoria dinâmica (só mostra as subcategorias da categoria selecionada)
    col_subcat = 'Sub-Category' if 'Sub-Category' in df.columns else 'Sub Category'
    df_temp_cat = df[df['Category'].isin(cat_sel)] if cat_sel else df
    subcategorias = df_temp_cat[col_subcat].unique()
    subcat_sel = st.sidebar.multiselect("Subcategoria", subcategorias, default=subcategorias)

    top_n = st.sidebar.slider("Top Cidades (Questão 4)", 5, 20, 10)

    # Aplicar TODOS os filtros selecionados ao DataFrame global
    mask = (
        (df['Order Date'].dt.date >= data_inicio) &
        (df['Order Date'].dt.date <= data_fim) &
        (df['Region'].isin(regiao_sel)) &
        (df['Segment'].isin(segmento_sel)) &
        (df['Category'].isin(cat_sel))
    )
    if subcat_sel:
        mask = mask & (df[col_subcat].isin(subcat_sel))

    df_filtrado = df[mask]

    # --- TÍTULO PRINCIPAL ---
    st.title("📊 Dashboard Superstore - ITA Jr.")

    # 2. Criando as 4 abas conforme a estrutura mínima do edital
    tab1, tab2, tab3, tab4 = st.tabs([
        "Visão Geral",
        "Perguntas 1 a 5",
        "Perguntas 6 a 10",
        "Conclusões & Recomendações"
    ])

    # ==========================================
    # ABA 1: VISÃO GERAL
    # ==========================================
    with tab1:
        st.header("Métricas Gerais do Negócio")

        # FIX: adicionadas 2 métricas extras para enriquecer a Visão Geral
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Vendas Totais", f"$ {df_filtrado['Sales'].sum():,.2f}")
        c2.metric("Lucro Total", f"$ {df_filtrado['Profit'].sum():,.2f}")
        c3.metric("Total de Pedidos", f"{df_filtrado['Order ID'].nunique():,}")
        c4.metric("Ticket Médio", f"$ {df_filtrado['Sales'].mean():,.2f}")

        st.subheader("Visualização Amostral dos Dados Filtrados")
        st.dataframe(df_filtrado.head(50), use_container_width=True)

        # BÔNUS: Botão para download de CSV
        st.markdown("---")
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados Filtrados em CSV",
            data=csv,
            file_name='dados_superstore_filtrados.csv',
            mime='text/csv',
        )

    # ==========================================
    # ABA 2: PERGUNTAS 1 A 5
    # ==========================================
    with tab2:
        st.header("Análise de Negócio - Questões 1 a 5")

        # Q1: Maior venda Office Supplies
        st.subheader("1. Cidade com maior valor de venda para 'Office Supplies'")
        df_q1 = df_filtrado[df_filtrado['Category'] == 'Office Supplies']
        if not df_q1.empty:
            res_q1 = df_q1.groupby('City')['Sales'].sum().idxmax()
            venda_q1 = df_q1.groupby('City')['Sales'].sum().max()
            st.success(f"A cidade líder é **{res_q1}** com um total de **$ {venda_q1:,.2f}** em vendas.")
        else:
            st.warning("Nenhum dado de 'Office Supplies' no período/filtro selecionado.")
        st.info("💡 **Insight:** Focar esforços de marketing e estoque de suprimentos nesta cidade polo pode otimizar os custos logísticos.")

        # Q2: Vendas por Data — GRÁFICO DE BARRAS (conforme edital)
        st.subheader("2. Total de Vendas por Data do Pedido")
        vendas_data = df_filtrado.groupby(df_filtrado['Order Date'].dt.date)['Sales'].sum().reset_index()
        fig2 = px.bar(
            vendas_data, x='Order Date', y='Sales',
            title="Vendas ao Longo do Tempo (Gráfico de Barras)",
            color_discrete_sequence=["#E1C51C"]
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.info("💡 **Insight:** O gráfico de barras evidencia o volume concentrado de compras em dias específicos, destacando os maiores picos comerciais.")

        # Q3: Vendas por Estado
        st.subheader("3. Total de Vendas por Estado")
        vendas_estado = df_filtrado.groupby('State')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
        fig3 = px.bar(
            vendas_estado, x='State', y='Sales', color='Sales',
            title="Faturamento por Unidade Federativa",
            color_continuous_scale=["#F3E26C", "#E1C51C", "#BA9E22"]
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.info("💡 **Insight:** Há uma forte concentração de receita em poucos estados líderes. Regiões periféricas possuem grande potencial inexplorado.")

        # Q4: Top N Cidades
        st.subheader(f"4. Top {top_n} Cidades em Vendas")
        vendas_cidade = df_filtrado.groupby('City')['Sales'].sum().nlargest(top_n).reset_index()
        fig4 = px.bar(
            vendas_cidade, x='Sales', y='City', orientation='h',
            title=f"Top {top_n} Cidades com Maior Faturamento",
            color_discrete_sequence=["#E1C51C"]
        )
        fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig4, use_container_width=True)
        st.info("💡 **Insight:** O ranking muda dinamicamente com os filtros laterais, evidenciando quais municípios sustentam o crescimento anual.")

        # Q5: Vendas por Segmento
        st.subheader("5. Proporção de Vendas por Segmento de Cliente")
        vendas_seg = df_filtrado.groupby('Segment')['Sales'].sum().reset_index()
        fig5 = px.pie(
            vendas_seg, values='Sales', names='Segment',
            title="Market Share por Segmentação",
            color_discrete_sequence=["#E1C51C", "#BA9E22", "#2A3A75"]
        )
        st.plotly_chart(fig5, use_container_width=True)
        st.info("💡 **Insight:** Mais da metade do faturamento provém de clientes finais (Consumer), validando estratégias focadas em varejo B2C.")

    # ==========================================
    # ABA 3: PERGUNTAS 6 A 10
    # ==========================================
    with tab3:
        st.header("Análise de Negócio - Questões 6 a 10")

        # Q6: Vendas por segmento e ano
        st.subheader("6. Total de Vendas por Segmento e Ano")
        q6_df = df_filtrado.groupby(['Year', 'Segment'])['Sales'].sum().reset_index()
        fig6 = px.bar(
            q6_df, x='Year', y='Sales', color='Segment', barmode='group',
            title="Vendas Anuais por Segmento",
            color_discrete_sequence=["#E1C51C", "#BA9E22", "#2A3A75"]
        )
        st.plotly_chart(fig6, use_container_width=True)
        st.info("💡 **Insight:** O segmento 'Consumer' mantém a liderança isolada ano após ano, mostrando-se a base mais resiliente da empresa.")

        # Q7 e Q8: Simulação Interativa de Desconto (BÔNUS: sliders)
        st.subheader("7 e 8. Simulação Interativa de Política de Descontos")

        col_s1, col_s2, col_s3 = st.columns(3)
        limite_valor = col_s1.slider("Valor Limite do Pedido ($)", 500, 5000, 1000, step=100)
        desc_alto = col_s2.slider("Desconto Acima do Limite (%)", 0, 50, 15) / 100.0
        desc_baixo = col_s3.slider("Desconto Abaixo do Limite (%)", 0, 50, 10) / 100.0

        # FIX: apenas um df_simulacao, calculado a partir dos sliders
        df_simulacao = df_filtrado.copy()
        df_simulacao['Desconto_Taxa'] = df_simulacao['Sales'].apply(
            lambda x: desc_alto if x > limite_valor else desc_baixo
        )
        df_simulacao['Venda_Com_Desconto'] = df_simulacao['Sales'] * (1 - df_simulacao['Desconto_Taxa'])

        qtd_pedidos_alto = (df_simulacao['Desconto_Taxa'] == desc_alto).sum()
        df_alto_desconto = df_simulacao[df_simulacao['Desconto_Taxa'] == desc_alto]

        media_antes = df_alto_desconto['Sales'].mean() if not df_alto_desconto.empty else 0
        media_depois = df_alto_desconto['Venda_Com_Desconto'].mean() if not df_alto_desconto.empty else 0

        # Q7
        st.markdown(f"👉 **Q7 — Resultado:** **{qtd_pedidos_alto}** pedidos possuem valor acima de **${limite_valor:,}** e receberiam desconto de **{desc_alto*100:.0f}%**.")

        # Q8 — FIX: apenas um bloco de métricas, sem duplicata
        c_sim1, c_sim2 = st.columns(2)
        c_sim1.metric(f"Média Original (Pedidos > ${limite_valor:,})", f"$ {media_antes:,.2f}")
        c_sim2.metric(f"Média com Desconto ({desc_alto*100:.0f}%)", f"$ {media_depois:,.2f}")

        st.info("💡 **Insight:** Com este simulador, o time de vendas pode descobrir o ponto de equilíbrio exato onde o desconto atrai grandes clientes sem comprometer drasticamente o ticket médio.")

        # Q9: Média de vendas por segmento, ano e mês
        st.subheader("9. Média de Vendas Mensal por Segmento e Ano")

        # FIX: usa cópia local para não mutar df_filtrado (evita SettingWithCopyWarning)
        q9_df = df_filtrado.copy()
        q9_df['Month'] = q9_df['Order Date'].dt.month
        q9_df = q9_df.groupby(['Year', 'Month', 'Segment'])['Sales'].mean().reset_index()

        fig9 = px.line(
            q9_df, x='Month', y='Sales', color='Segment', facet_col='Year', markers=True,
            title="Evolução da Média de Vendas: Meses (Eixo X) subdivididos por Ano",
            color_discrete_sequence=["#E1C51C", "#BA9E22", "#2A3A75", "#F3E26C"]
        )
        fig9.update_xaxes(tickmode='array', tickvals=list(range(1, 13)))
        st.plotly_chart(fig9, use_container_width=True)
        st.info("💡 **Insight:** Separando a visão por ano, fica claro que o comportamento de compras não é uniforme. Meses como outubro e novembro frequentemente puxam a média para cima devido ao aquecimento de fim de ano.")

        # Q10: Top 12 Subcategorias em Vendas
        st.subheader("10. Vendas por Categoria e Subcategoria (Top 12)")
        col_subcat_q10 = 'Sub-Category' if 'Sub-Category' in df_filtrado.columns else 'Sub Category'

        if col_subcat_q10 in df_filtrado.columns:
            q10_df = df_filtrado.groupby(['Category', col_subcat_q10])['Sales'].sum().reset_index()
            top12_sub = q10_df.nlargest(12, 'Sales')
            fig10 = px.bar(
                top12_sub, x='Sales', y=col_subcat_q10, color='Category', orientation='h',
                title="Top 12 Subcategorias mais Rentáveis",
                color_discrete_sequence=["#E1C51C", "#BA9E22", "#2A3A75"]
            )
            fig10.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig10, use_container_width=True)
            st.info("💡 **Insight:** Cadeiras (Chairs) e Telefones (Phones) disparam na frente. Produtos de tecnologia e mobiliário corporativo sustentam o faturamento grosso devido ao alto valor unitário.")
        else:
            st.error("Coluna de subcategoria não encontrada no banco.")

    # ==========================================
    # ABA 4: CONCLUSÕES & RECOMENDAÇÕES
    # ==========================================
    with tab4:
        st.header("🧠 Conclusões e Recomendações Estratégicas")
        st.markdown("""
        ### Diagnóstico do Negócio
        * **Dependência de Varejo:** O segmento *Consumer* representa a maior fatia do faturamento. A empresa está muito exposta a oscilações do mercado consumidor direto.
        * **Concentração Geográfica:** Poucos estados geram a maior parte do lucro, sugerindo que o modelo de expansão logística precisa ser revisado para as demais regiões.
        * **Produtos Âncora:** Tecnologia (*Phones*) e Mobiliário (*Chairs*) carregam a receita da empresa nas costas.

        ### Recomendações Técnicas e de Negócio
        1. **Ajuste na Política de Descontos:** A simulação (Questões 7 e 8) provou que dar 15% de desconto linear para pedidos acima de $1.000 corrói margens valiosas de produtos premium. O ideal é criar um teto progressivo baseado na recorrência do comprador.
        2. **Sazonalidade:** Aproveitar os vales de venda mapeados na série histórica (Questão 9) para realizar queimas de estoque programadas de subcategorias com menor giro.
        """)

        st.markdown("---")
        st.subheader("⚠️ Limitações dos Dados e Erros Comuns")
        st.markdown("""
        * **Outliers e Valores Extremos:** O banco de dados possui compras atípicas (ex: Corporate no final do ano) que podem distorcer as médias mensais calculadas na análise.
        * **Custos Ocultos:** A base informa *Sales* (Receita) e *Profit* (Lucro), mas não discrimina os custos operacionais, logísticos ou impostos. Portanto, o lucro reportado não é o lucro líquido final (DRE completo).
        * **Incompletude Temporal:** Dependendo dos filtros de data aplicados no menu lateral, certas sazonalidades anuais podem ser cortadas pela metade, afetando os gráficos de linha.
        """)