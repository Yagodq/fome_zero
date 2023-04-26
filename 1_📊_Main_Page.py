#Bibliotecas
import pandas as pd
import plotly.express as px
import numpy as np
import inflection
import streamlit as st
import folium 
from PIL import Image
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

#Comando para juntar as páginas
st.set_page_config( page_title="Main Page", page_icon="📊", layout='wide')

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

def create_map ( df1 ):
    """ Cria um mapa com marcadores que identificam os restaurantes da base de dados.
        imput:Dataframe
        output:Mapa da biblioteca folium
    """
    #Cria um mapa
    map = folium.Map(max_bounds=True)
    # Adiciona agrupamentos de popup
    marker_cluster = MarkerCluster().add_to(map)
    # Percore as localizações e cria um marcador para cada
    for index, location_info in df1.iterrows():    
        folium.Marker( [location_info["latitude"], location_info["longitude"]], 
                    popup=location_info[['restaurant_name','cuisines']],
                    icon=folium.Icon(color=location_info['color_type'] ,icon="home", prefix="fa"),
                    ).add_to(marker_cluster)
    return map 

#-------------------------------------------------------------------------------------------------
#-------------------------------- Inicío da estrutura lógica do código ---------------------------
#Lendo arquivo .csv, Importando Dataset
df = pd.read_csv('dataset\zomato.csv')

#Cópia do dataframe original
df1 = df.copy() 

#Limpeza dos dados
df1 = clean_code( df )

#=========================================================
#Barra lateral Streamlit
#=========================================================

st.title( 'Fome Zero!' )
st.header('O melhor lugar para encontrar seu mais novo restaurante favorito!')
#Recebe a imagem do logo
image_path = 'logo.jpg'
image =Image.open( image_path)
# Cria uma coluna com a imagem e o texto
col1, col2 = st.sidebar.columns([1, 2], gap="small")
col1.image(image, width=80)
col2.markdown("# Fome Zero")
st.sidebar.markdown( """___""")

#Filtro país
st.sidebar.markdown( '## Filtros:')
country_options = st.sidebar.multiselect('Escolha os Paises que Deseja visualizar as Informações:',
    df1.loc[:,'country'].unique().tolist(),
    default=df1.loc[:,'country'].unique().tolist())
st.sidebar.markdown( """___""")

#Filtro de país
#Usado o comando isin, passando que as opções do filtro estão em algum lugar
linhas_selecionadas = df1['country'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, :]

#=========================================================
#Layout Streamlit
#=========================================================
with st.container():
    st.markdown('### Métricas gerais da plataforma:')
    st.markdown( """___""")
    #Criação de 6 colunas para divisão dos métricas
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    #Coluna restaurantes únicos
    with col1:
        df_aux = df1.loc[:, 'restaurant_id'].nunique()
        col1.metric('Restaurantes cadastrados', df_aux)
    #Coluna países cadastrados
    with col2:
        df_aux = df1.loc[:, 'country'].nunique()
        col2.metric('Países cadastrados', df_aux)      
    # Cidades cadastradas
    with col3:
        df_aux = df1.loc[:, 'city'].nunique()
        col3.metric('Cidades cadastradas', df_aux) 
    # Avaliaçoes feitas na plataforma
    with col4: 
        df_aux = df1.loc[:, 'votes'].sum()
        col4.metric('Avaliações feitas na plataforma', df_aux)
    # Tipos culinários
    with col5:
        df_aux = df1.loc[:, 'cuisines'].nunique()
        col5.metric('Tipos de culinária oferecidos', df_aux)
    # Tipos de moeda aceitos
    with col6: 
        df_aux = df1.loc[:, 'currency'].nunique()
        col6.metric('Tipos de moeda aceitos', df_aux)
st.markdown( """___""")

with st.container():
    map = create_map ( df1)
    #Comando para exibição de mapa no Streamlit
    folium_static( map, width=1024, height=768)


   