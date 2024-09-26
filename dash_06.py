import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações gerais
st.set_page_config(page_title="Dashboard de Imóveis para Aluguel", layout="wide")
st.title("Análise Completa de Imóveis para Aluguel")

# Lmpar colunas de moeda
def limpar_coluna_moeda(coluna):
    if df[coluna].dtype == 'object':  # Se for do tipo string
        df[coluna] = df[coluna].str.replace('R$', '').str.replace(',', '').astype(float)
    return df[coluna]

# Carregar e limpar os dados
df = pd.read_csv('houses_to_rent_v2.csv')

df['valor_aluguel'] = limpar_coluna_moeda('rent amount (R$)')
df['valor_total'] = limpar_coluna_moeda('total (R$)')
df['condominio'] = limpar_coluna_moeda('hoa (R$)')
df['iptu'] = limpar_coluna_moeda('property tax (R$)')
df['seguro_incendio'] = limpar_coluna_moeda('fire insurance (R$)')

# Filtro na barra lateral
st.sidebar.header("Filtro de Cidades")
cidades_selecionadas = st.sidebar.multiselect("Escolha as cidades:", df['city'].unique(), default=df['city'].unique())
df_filtrado = df[df['city'].isin(cidades_selecionadas)]

# Cores e estilo
sns.set(style="whitegrid", palette="muted")
paleta_cidades = sns.color_palette("Set2", len(df_filtrado['city'].unique()))

# Primeira linha de gráficos
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Aluguel por Cidade")
    fig, ax = plt.subplots()
    sns.boxplot(x='city', y='valor_aluguel', data=df_filtrado, ax=ax, palette=paleta_cidades)
    ax.set_title("Distribuição do Aluguel por Cidade")
    st.pyplot(fig)

with col2:
    st.subheader("Total de Despesas por Cidade")
    fig, ax = plt.subplots()
    sns.boxplot(x='city', y='valor_total', data=df_filtrado, ax=ax, palette=paleta_cidades)
    ax.set_title("Distribuição das Despesas Totais")
    st.pyplot(fig)

with col3:
    st.subheader("Banheiros vs. Aluguel")
    fig, ax = plt.subplots()
    sns.scatterplot(x='bathroom', y='valor_aluguel', hue='city', data=df_filtrado, ax=ax, palette=paleta_cidades)
    ax.set_title("Correlação entre Banheiros e Aluguel")
    st.pyplot(fig)

# Segunda linha de gráficos
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("IPTU por Cidade")
    fig, ax = plt.subplots()
    sns.boxplot(x='city', y='iptu', data=df_filtrado, ax=ax, palette=paleta_cidades)
    ax.set_title("Distribuição do IPTU")
    st.pyplot(fig)

with col5:
    st.subheader("Imóveis Mobiliados vs. Não Mobiliados")
    conteudo_mobiliado = df_filtrado['furniture'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(conteudo_mobiliado, labels=conteudo_mobiliado.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.set_title("Comparação de Mobiliados")
    st.pyplot(fig)

with col6:
    st.subheader("Aceitação de Animais por Cidade")
    animais_por_cidade = df_filtrado.groupby(['city', 'animal']).size().unstack().fillna(0)
    fig, ax = plt.subplots()
    animais_por_cidade.plot(kind='bar', stacked=True, ax=ax, color=sns.color_palette("Set2", 2))
    ax.set_title("Aceitação de Animais")
    st.pyplot(fig)

# Terceira linha de gráficos
col7, col8, col9 = st.columns(3)

with col7:
    st.subheader("Aluguel vs. Aceitação de Animais")
    fig, ax = plt.subplots()
    sns.boxplot(x='animal', y='valor_aluguel', data=df_filtrado, ax=ax, palette=sns.color_palette("coolwarm", 2))
    ax.set_title("Correlação entre Aluguel e Animais")
    st.pyplot(fig)

with col8:
    st.subheader("Condomínio por Cidade")
    fig, ax = plt.subplots()
    sns.boxplot(x='city', y='condominio', data=df_filtrado, ax=ax, palette=paleta_cidades)
    ax.set_title("Taxa de Condomínio")
    st.pyplot(fig)

with col9:
    st.subheader("Imóveis Mobiliados por Cidade")
    mobiliados_por_cidade = df_filtrado[df_filtrado['furniture'] == 'furnished'].groupby('city').size()
    st.bar_chart(mobiliados_por_cidade)

# Quarta linha de gráficos
col10, col11 = st.columns(2)

with col10:
    st.subheader("Comparação de Aluguel, Condomínio e IPTU")
    fig, ax = plt.subplots()
    sns.boxplot(data=df_filtrado[['valor_aluguel', 'condominio', 'iptu']], ax=ax, palette=sns.color_palette("husl", 3))
    ax.set_title("Comparação de Valores")
    st.pyplot(fig)

with col11:
    st.subheader("Seguro Incêndio por Cidade")
    fig, ax = plt.subplots()
    sns.boxplot(x='city', y='seguro_incendio', data=df_filtrado, ax=ax, palette=paleta_cidades)
    ax.set_title("Seguro Incêndio por Cidade")
    st.pyplot(fig)

# Insights Finais
st.write("### Insights Principais:")
st.write("""
- **Valor de Aluguel**: São Paulo continua se destacando com os aluguéis mais elevados, enquanto outras cidades como Campinas têm valores medianos mais baixos.
- **Taxas**: O valor do condomínio varia significativamente entre as cidades, sendo importante considerar essa variável.
- **Aceitação de Animais**: Imóveis que aceitam animais apresentam maior variabilidade no valor do aluguel.
- **Mobiliados**: A oferta de imóveis mobiliados é mais comum em algumas cidades e pode influenciar na escolha do imóvel.
""")
