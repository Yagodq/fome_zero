#Bibliotecas
import pandas as pd
import plotly.express as px
import numpy as np
import inflection
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Cuisines", page_icon="🍽️", layout="wide")

##-------------------- Funções---------------------
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    """ Prenche os nomes do países com base no country_code
        imput:Dataframe
        output:Dataframe
    """
    return COUNTRIES[country_id]

def create_price_tye(price_range):
    """ Criação de coluna de categoria de comida
        imput:Dataframe
        output:Dataframe
    """
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    """ Cria a coluna com nome das cores 
        imput:Dataframe
        output:Dataframe
    """
    return COLORS[color_code]


def rename_columns(dataframe):
    """ Renomeia as colunas do dataframe
        imput:Dataframe
        output:Dataframe
    """
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe
        tipos de limpeza:
        Transformação dos códigos de país em nomes
        Criação de coluna de categoria apartir do price_range
        Criação de coluna de cores apartir de ranting_color
        Categorização da coluna cuisines em somente um tipo culinário
        Conversão de colunas númericas para categoricas
        Remoção de linhas duplicadas
        Remoção de colunas irrelevantes
        Imput:Dataframe
        Output:Dataframe
    """   
    #Renomeia os nomes da colunas 
    df1 = rename_columns( df )
    #Transforma os código em países 
    df1['country'] = df1['country_code'].apply(country_name)
    #Cria coluna de categoria de comida
    df1['price_type'] = df1['price_range'].apply(create_price_tye)
    #Cria nome das cores
    df1['color_type'] = df1['rating_color'].apply(color_name)
    #Categoriza a coluna cuisines para somente um tipo de culinára
    df1.loc[:, 'cuisines'] = df1.loc[:, 'cuisines'].astype(str).apply(lambda x: x.split(',')[0])
    #Conversão de númericos para categoricos
    df1['table_booking'] = pd.cut(df1['has_table_booking'], bins=2, labels=['sim', 'nao'])
    df1['online_delivery'] = pd.cut(df1['has_online_delivery'], bins=2, labels=['sim', 'nao'])
    df1['delivering_now'] = pd.cut(df1['is_delivering_now'], bins=2, labels=['sim', 'nao'])
    # Eliminando linhas duplicadas do dataframe
    df1.drop_duplicates(inplace=True)
    # Elimina colunas irrelevante do dataframe
    df1 = (df1.drop([ 'country_code','rating_color', 'price_range', 'switch_to_order_menu', 
                      'has_table_booking', 'has_online_delivery', 'is_delivering_now', 'address', 'locality_verbose' ], axis=1))
    return df1

def top_restaurant_rating( df1 ):
    """ Retorna quadro com top 15 restaurantes por maior quantidade de votos e avaliação.
        imput:Dataframe
        output:dataframe
    """
    # Agrupa os restaurantes com maior nota média 
    df_aux = (df1.loc[:,['restaurant_id','restaurant_name', 'cuisines','aggregate_rating','country','votes']]
              .sort_values(['aggregate_rating','votes'], ascending=[False, False]).head(15))
    return df_aux

def cuisines_bar( df1, col, operacao, label_name):
    """ Produz um gráfico de barras, demonstrando a avaliação média por país.
    imput:Dataframe
    Parametros: col: Modifica a coluna a sofrer as operação
                    'restaurant_id': Retorna a coluna restaurante_id
                    'aggregate_rating': Retorna a coluna de avaliação
                label_name: Modificar o nome da coluna no gráfico
                    'Restaurantes registrados': Exibe a frase
                    'Avaliação média'': Exibe a frase
                operacao: Modifica a operação aplicada sobre as colunas
                    count: Soma os valores
                    mean: Calcula a média aritmética 
                    
    output:Gráfico de barra
    """
    ## Agrupa os tipos culinarios pela maior nota media
    df_aux = df1.loc[:, [ col , 'cuisines']].groupby('cuisines').agg(operacao).sort_values( col , ascending=False).reset_index().head(15)
    # Gráfico de barras
    fig = px.bar(df_aux, x='cuisines', y= col, text_auto=True, 
                 color='cuisines',labels={ col : label_name, 'cuisines': 'Tipos culinários'})
    return fig


#-------------------------------------------------------------------------------------------------
#-------------------------------- Inicío da estrutura lógica do código ---------------------------
#Lendo arquivo .csv, Importando Dataset
df = pd.read_csv('zomato.csv')

#Cópia do dataframe original
df1 = df.copy() 

#Limpeza dos dados
df1 = clean_code( df )

# Cuisines ===========================================

#=========================================================
#Barra lateral Streamlit
#=========================================================

st.title( '🍽️ Visão Tipos de Cozinhas' )
#Recebe a imagem do logo
image_path = 'logo.jpg'
image =Image.open( image_path)
# Cria uma coluna com a imagem e o texto
col1, col2 = st.sidebar.columns([1, 2], gap="small")
col1.image(image, width=80)
col2.markdown("# Fome Zero")
st.sidebar.markdown( """___""")

st.sidebar.markdown( '## Filtros:')
#Filtro país
country_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar as Informações:',
    df1.loc[:,'country'].unique().tolist(),
    default= df1.loc[:,'country'].unique().tolist())
#Filtro cozinhas
cuisines_options = st.sidebar.multiselect(
    'Escolha o tipo culinário que Deseja visualizar as Informações:',
    df1.loc[:,'cuisines'].unique().tolist(),
    default= df1.loc[:,'cuisines'].unique().tolist())
st.sidebar.markdown( """___""")

#Filtro de cozinha
#Usado o comando isin, passando que as opções do filtro estão em algum lugar
linhas_selecionadas = df1['cuisines'].isin( cuisines_options )
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de país
#Usado o comando isin, passando que as opções do filtro estão em algum lugar
linhas_selecionadas = df1['country'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, :]

#=========================================================
#Layout Streamlit
#=========================================================
# Top 15 melhores restaurantes por tipo culinários
with st.container():
    df_aux = top_restaurant_rating( df1 )
    st.markdown('##### Top 15 restaurantes por quantidade e nota das avaliações')
    st.dataframe(df_aux)
with st.container():
    fig = cuisines_bar( df1, col='aggregate_rating', operacao='mean', label_name='Avaliação média')
    st.markdown('##### Top 15 tipos de culinária com maior média de avaliação')
    st.plotly_chart( fig)    
with st.container():
    fig = cuisines_bar( df1, col='restaurant_id', operacao='count', label_name='Restaurantes registrados')
    st.markdown('##### Top 15 tipos de culinária com mais restaurantes na base de dados')
    st.plotly_chart( fig )
      
    
    
