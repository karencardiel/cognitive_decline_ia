import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

# 1. configuracion de la pagina y recursos
st.set_page_config(page_title="Análisis de IA y Cognición", layout="wide")

# cargar stopwords (se ejecuta solo una vez)
@st.cache_resource
def load_nltk_stopwords():
    try:
        stopwords.words('spanish')
    except LookupError:
        nltk.download('stopwords')
load_nltk_stopwords()


# 2. titulo y descripcion del dashboard
st.title('📊 Dashboard de Sentimientos y Habilidades Cognitivas')
st.write("""
Visualiza los sentimientos y habilidades cognitivas más mencionadas en videos de YouTube sobre inteligencia artificial.
""")


# 3. carga y filtrado de datos
@st.cache_data
def cargar_datos():
    # carga los datos desde el archivo csv
    try:
        df = pd.read_csv("comentarios_con_sentimiento.csv")
        if "insight" in df.columns:
            return df[df["insight"] != "sin categoría"].copy()
        return df
    except FileNotFoundError:
        st.error("Error: No se encontró el archivo 'comentarios_con_sentimiento.csv'. Por favor, ejecuta primero el script 'procesar_comentarios.py'.")
        return pd.DataFrame()

df = cargar_datos()
df_filtrado = df.copy()

# 4. barra lateral con filtros
with st.sidebar:
    st.header("Filtros")
    if not df.empty:
        opcion_sentimiento = st.selectbox(
            "Selecciona un sentimiento",
            ["Todos"] + df["sentimiento"].unique().tolist()
        )
        opcion_insight = st.selectbox(
            "Selecciona una habilidad cognitiva",
            ["Todos"] + sorted(df["insight"].unique())
        )

        # aplicacion de filtros
        if opcion_sentimiento != "Todos":
            df_filtrado = df_filtrado[df_filtrado["sentimiento"] == opcion_sentimiento]
        if opcion_insight != "Todos":
            df_filtrado = df_filtrado[df_filtrado["insight"] == opcion_insight]


# 5. cuerpo principal del dashboard

if not df_filtrado.empty:
    st.header('Métricas Clave')
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Comentarios Analizados", value=len(df_filtrado))
    col2.metric(label="Score Promedio de Sentimiento", value=f"{df_filtrado['score'].mean():.2f}")
    col3.metric(label="Habilidades Únicas Detectadas", value=df_filtrado["insight"].nunique())

    st.markdown("---")
    
    st.header('Gráficos de Distribución')
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader('Distribución de Sentimientos')
        sentiment_data = df_filtrado['sentimiento'].value_counts().reset_index()
        fig1, ax1 = plt.subplots()
        sns.barplot(data=sentiment_data, x='sentimiento', y='count', hue='sentimiento', ax=ax1, palette="viridis", legend=False)
        ax1.set_title('Conteo de Comentarios por Sentimiento')
        ax1.set_xlabel('Sentimiento')
        ax1.set_ylabel('Número de Comentarios')
        st.pyplot(fig1)

    with col_chart2:
        st.subheader('Distribución de Habilidades Cognitivas')
        insight_data = df_filtrado['insight'].value_counts().reset_index()
        fig2, ax2 = plt.subplots()
        sns.barplot(data=insight_data, x='insight', y='count', hue='insight', ax=ax2, palette="plasma", legend=False)
        ax2.set_title('Menciones de Habilidades Cognitivas')
        ax2.set_xlabel('Habilidad Cognitiva')
        ax2.set_ylabel('Número de Menciones')
        # rotar etiquetas para que no se sobrepongan
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig2)
        
    st.markdown("---")

    # nube de palabras
    st.header('Nube de Palabras Clave')
    texto_completo = " ".join(df_filtrado['texto'].dropna().astype(str)).lower()
    if texto_completo.strip():
        spanish_stopwords = set(stopwords.words('spanish'))
        # tu lista personalizada de stopwords
        additional_stopwords = {
            "asi", "tan", "mucho", "mucha", "poco", "poca", "vez", "veces", "siempre", "nunca",
            "ahora", "antes", "despues", "de", "que", "la", "lo", "un", "si", "e", "eso", "como",
            "luego", "cada", "digo", "saludo", "debe", "mismo", "va", "gracia", "pido", "aldo", 
            "ademas", "pues", "parte", "incluso", "entonces", "anque", "muchas", "gracias", "alguien", 
            "ma", "realmente", "cualquier", "etc", "simplemente", "aun", "q", "sido", "cosa", "solo", "video", "puede"
        }
        all_stopwords = spanish_stopwords.union(additional_stopwords)

        wordcloud = WordCloud(
            width=1200, height=600, background_color="white", colormap='cividis',
            max_words=150, stopwords=all_stopwords, collocations=False
        ).generate(texto_completo)

        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)

    st.markdown("---")

    # explorador de datos crudos
    with st.expander("Explora los Datos Filtrados", expanded=False):
        st.dataframe(df_filtrado)
else:
    st.warning("No se encontraron datos para los filtros seleccionados. Por favor, ajusta tu selección.")