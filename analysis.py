import pandas as pd
import streamlit as st
import plotly.express as px
import ast

# Carregar dataset
df = pd.read_csv("steam_games.csv")

generos_jogos = [
    "Indie", "Action", "Adventure", "Casual", "Simulation", "RPG", "Strategy",
    "Early Access", "Free To Play", "Sports", "Racing", "Massively Multiplayer",
    "Violent", "Gore", "Nudity", "Sexual Content"
]

def normalizar_genero(genero):
    if genero not in generos_jogos:
        return "Software"
    return genero


df["platforms"] = df["platforms"].apply(ast.literal_eval)

df_genres = df.copy()
df_genres["genres"] = df_genres["genres"].apply(eval)
df_genres = df_genres.explode("genres")
df_genres["genres"] = df_genres["genres"].apply(normalizar_genero)

df_categories = df.copy()
df_categories["categories"] = df_categories["categories"].apply(eval)
df_categories = df_categories.explode("categories")

st.set_page_config(page_title="Steam Dashboard", layout="wide")
st.title("Análise de Jogos da Steam")

opcoes = [
    "Maior Média de Nota no Metacritic",
    "Maiores Preços (Sem Gratuitos)",
    "Maior Média de Conquistas",
    "Maior Percentual de Avaliações Positivas"
]
opcao_escolhida = st.selectbox("Escolha a Métrica:", opcoes)

col1, col2 = st.columns(2)

def calcular_metricas(df, coluna):
    if opcao_escolhida == "Maior Média de Nota no Metacritic":
        return df[df["metacritic"] > 0].groupby(coluna)["metacritic"].mean().sort_values(ascending=False)
    elif opcao_escolhida == "Maiores Preços (Sem Gratuitos)":
        return df[df["price_initial (USD)"] > 0].groupby(coluna)["price_initial (USD)"].mean().sort_values(ascending=False)
    elif opcao_escolhida == "Maior Média de Conquistas":
        return df[df["n_achievements"] > 0].groupby(coluna)["n_achievements"].mean().sort_values(ascending=False)
    elif opcao_escolhida == "Maior Percentual de Avaliações Positivas":
        return df[df["positive_percentual"] > 0].groupby(coluna)["positive_percentual"].mean().sort_values(ascending=False)

with col1:
    st.subheader("Por Gênero")
    metricas_generos = calcular_metricas(df_genres, "genres")
    fig1 = px.bar(
        x=metricas_generos.index,
        y=metricas_generos.values,
        labels={"x": "Gênero", "y": opcao_escolhida},
        color=metricas_generos.index  # <- ESSA LINHA AQUI
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Por Categoria")
    metricas_categorias = calcular_metricas(df_categories, "categories")
    fig2 = px.bar(
        x=metricas_categorias.index,
        y=metricas_categorias.values,
        labels={"x": "Categoria", "y": opcao_escolhida},
        color=metricas_categorias.index  # <- ESSA LINHA AQUI
    )
    st.plotly_chart(fig2, use_container_width=True)


st.markdown("---")
st.subheader("Distribuições Gerais dos Jogos")

opcao_pizza = st.selectbox("Escolha o tipo de distribuição:", [
    "Distribuição por Gênero",
    "Distribuição por Faixa de Preço",
    "Distribuição de Plataformas"
])

if opcao_pizza == "Distribuição por Gênero":
    genero_contagem = df_genres["genres"].value_counts()
    fig_pizza = px.pie(names=genero_contagem.index, values=genero_contagem.values)

elif opcao_pizza == "Distribuição por Faixa de Preço":
    def faixa_preco(preco):
        if preco == 0:
            return "Gratuito"
        elif preco <= 10:
            return "$0.01 - $10"
        elif preco <= 30:
            return "$10.01 - $30"
        elif preco <= 50:
            return "$30.01 - $50"
        else:
            return "Acima de $50"

    df["faixa_preco"] = df["price_initial (USD)"].apply(faixa_preco)
    contagem_faixa = df["faixa_preco"].value_counts()
    fig_pizza = px.pie(names=contagem_faixa.index, values=contagem_faixa.values)

elif opcao_pizza == "Distribuição de Plataformas":
    def classificar_plataforma(plataformas):
        if not plataformas:
            return "Desconhecido"
        plataformas = set(plataformas)
        if plataformas == {"windows"}:
            return "Exclusivo Windows"
        elif plataformas == {"mac"}:
            return "Exclusivo Mac"
        elif plataformas == {"linux"}:
            return "Exclusivo Linux"
        elif len(plataformas) > 1:
            return "Multiplataforma"
        else:
            return "Outros"

    df["class_plataforma"] = df["platforms"].apply(classificar_plataforma)
    contagem_plataformas = df["class_plataforma"].value_counts()

    fig_pizza = px.pie(
        names=contagem_plataformas.index,
        values=contagem_plataformas.values,
        title="Distribuição de Plataformas"
    )

st.plotly_chart(fig_pizza, use_container_width=True)

# Opção para escolher o tipo de avaliação
opcao_avaliacao = st.selectbox("Escolha o tipo de avaliação:", [
    "Avaliação dos Usuários (Steam)",
    "Nota Metacritic"
])


if opcao_avaliacao == "Avaliação dos Usuários (Steam)":
    coluna_avaliacao = "review_score"
    nome_legenda = "Avaliação dos Usuários"
else:
    coluna_avaliacao = "metacritic"
    nome_legenda = "Nota Metacritic"

# Filtra valores válidos e arredonda a nota
df_validos = df[df[coluna_avaliacao] > 0].copy()
df_validos["nota_arredondada"] = df_validos[coluna_avaliacao].round()

# Agrupa por nota arredondada e conta quantos jogos existem em cada faixa
qtd_por_nota = df_validos["nota_arredondada"].value_counts().sort_index().reset_index()
qtd_por_nota.columns = [nome_legenda, "Quantidade de Jogos"]


fig_qtd = px.line(
    qtd_por_nota,
    x=nome_legenda,
    y="Quantidade de Jogos",
    markers=True,
    title=f"Quantidade de Jogos por {nome_legenda}",
    labels={
        nome_legenda: nome_legenda,
        "Quantidade de Jogos": "Qtd de Jogos"
    }
)

st.plotly_chart(fig_qtd, use_container_width=True)
