🎮 Steam Games Dashboard
Dashboard interativo criado com Python, Streamlit e Plotly, com foco em análise visual de jogos disponíveis na Steam. A aplicação permite explorar diferentes métricas dos jogos por gênero, categoria, plataformas e faixa de preço.

📊 Funcionalidades
🔍 Comparação por Métricas:
Você pode escolher uma entre as seguintes métricas para comparar os jogos:

🎯 Maior Média de Nota no Metacritic

💸 Maiores Preços (excluindo jogos gratuitos)

🏆 Maior Média de Conquistas

👍 Maior Percentual de Avaliações Positivas

Essas métricas são apresentadas de duas formas:

Por Gênero

Por Categoria

🧩 Distribuições Gerais:
Três tipos de gráficos de pizza estão disponíveis para entender a composição da base de dados:

Distribuição por Gênero

Distribuição por Faixa de Preço

Distribuição de Plataformas (Windows, Mac, Linux ou Multiplataforma)

📈 Avaliação dos Jogos:
Exibe um gráfico de linha com a quantidade de jogos para cada faixa de nota:

Nota Metacritic

Avaliação dos Usuários da Steam

🚀 Como Executar o Projeto
1- Clone o repositório ou baixe os arquivos:

pip install pandas streamlit plotly

2- Instale as dependências:

pip install pandas streamlit plotly

3- Execute o dashboard:

streamlit run dashboard.py


🧠 Bibliotecas Utilizadas
pandas – Manipulação de dados

streamlit – Criação da interface interativa

plotly.express – Visualizações de gráficos (barras, pizza, linha)

ast – Conversão de strings para listas reais (colunas como gêneros e plataformas)

⚙️ Observações Técnicas
O dataset deve estar nomeado como steam_games.csv no mesmo diretório.

O campo "platforms" é tratado como lista de strings.

Gêneros desconhecidos são agrupados na categoria "Software".

Jogos com valores zero nas métricas , exeto o preço dos gratuitos, são automaticamente filtrados.



