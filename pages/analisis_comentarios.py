import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import os

# Título del dashboard específico de la página
st.title('📊 Dashboard de sentimientos y habilidades cognitivas')
st.write("Visualiza los sentimientos y habilidades cognitivas más mencionadas en videos de YouTube sobre inteligencia artificial.")

# Función para asegurar que NLTK tiene las stopwords
@st.cache_resource
def load_nltk_stopwords():
    try:
        stopwords.words('spanish')
    except LookupError:
        nltk.download('stopwords')
load_nltk_stopwords()

# Función para cargar los datos
@st.cache_data
def cargar_datos():
    file_path = "comentarios_con_sentimiento.csv"
    if not os.path.exists(file_path):
        st.error(f"Error: No se encontró el archivo '{file_path}'. Ejecuta primero el script 'procesar_comentarios.py' desde tu terminal.")
        return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    if "insight" in df.columns:
        return df[df["insight"] != "sin categoría"].copy()
    return df

df = cargar_datos()

if not df.empty:
    df_filtrado = df.copy()

    # Barra lateral con filtros
    with st.sidebar:
        st.header("Filtros de Comentarios")
        opcion_sentimiento = st.selectbox(
            "Selecciona un sentimiento",
            ["Todos"] + df["sentimiento"].unique().tolist()
        )
        opcion_insight = st.selectbox(
            "Selecciona una habilidad cognitiva",
            ["Todos"] + sorted(df["insight"].unique())
        )

        if opcion_sentimiento != "Todos":
            df_filtrado = df_filtrado[df_filtrado["sentimiento"] == opcion_sentimiento]
        if opcion_insight != "Todos":
            df_filtrado = df_filtrado[df_filtrado["insight"] == opcion_insight]

    # Cuerpo principal del dashboard
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
            st.pyplot(fig1)

        with col_chart2:
            st.subheader('Distribución de Habilidades Cognitivas')
            insight_data = df_filtrado['insight'].value_counts()
            fig2, ax2 = plt.subplots()
            sns.barplot(x=insight_data.index, y=insight_data.values, hue=insight_data.index, ax=ax2, palette="plasma", legend=False)
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig2)
            
        st.markdown("---")

        st.header('Nube de Palabras Clave')
        texto_completo = " ".join(df_filtrado['texto'].dropna().astype(str)).lower()
        if texto_completo.strip():
            spanish_stopwords = set(stopwords.words('spanish'))
            additional_stopwords = {"q", "si", "de", "la", "el", "en", "un", "una", "los", "las", "que", "es", "por", "para", "con", "del", "al", "etc", "cosas", "sino", "veces",
                                    "siento", "pasa", "tener", "gracias", "Freddy", "pueden", "usan", "video", "sido", "entiendo", "cómo", "ello", "entonces", "creo", "pues", "dice",
                                    "simplemente", "va", "mas", "cada", "veo", "toda", "vez", "da", "realmente", "dices", "debe", "parte", "voy", "tan", "quieren" 
            }
            all_stopwords = spanish_stopwords.union(additional_stopwords)

            wordcloud = WordCloud(width=1200, height=600, background_color="white", colormap='cividis', max_words=150, stopwords=all_stopwords, collocations=False).generate(texto_completo)
            fig_wc, ax_wc = plt.subplots()
            ax_wc.imshow(wordcloud, interpolation='bilinear')
            ax_wc.axis("off")
            st.pyplot(fig_wc)

        with st.expander("Explora los Datos Filtrados", expanded=False):
            st.dataframe(df_filtrado)
    else:
        st.warning("No se encontraron datos para los filtros seleccionados.")