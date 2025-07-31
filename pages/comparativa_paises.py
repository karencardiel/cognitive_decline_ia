import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title('🌎 Dashboard comparativo del uso de IA en la educación')
st.write("Análisis comparativo sobre el uso y conocimiento de IA entre estudiantes de Bangladesh, India, Rumania y Turquía.")

@st.cache_data
def load_and_prepare_data():
    files = ['bangladesh.csv', 'india.csv', 'rumania.csv', 'turkey.csv']
    for file in files:
        if not os.path.exists(file):
            st.error(f"Error: No se encontró el archivo '{file}'. Asegúrate de que todos los archivos CSV estén en el directorio principal.")
            return None, None, {}

    bangladesh_df = pd.read_csv('bangladesh.csv')
    india_df = pd.read_csv('india.csv')
    romania_df = pd.read_csv('rumania.csv')
    turkey_df = pd.read_csv('turkey.csv')
    
    all_dfs = {'Bangladesh': bangladesh_df, 'India': india_df, 'Rumania': romania_df, 'Turquía': turkey_df}
    
    # Normalización (código original sin cambios)
    bangladesh_usage_map = {'Never': 0, 'Occasionally': 0.25, 'Monthly': 0.5, 'Weekly': 0.75, 'Daily': 1}
    bangladesh_df['AI_Usage_Normalized'] = bangladesh_df[bangladesh_df.columns[2]].map(bangladesh_usage_map)
    bangladesh_df['Country'] = 'Bangladesh'

    india_df['AI_Usage_Normalized'] = pd.to_numeric(india_df[india_df.columns[5]], errors='coerce').apply(lambda x: 0.25 if x < 1 else (0.5 if 1 <= x <= 3 else 1))
    india_df['AI_Knowledge_Normalized'] = (pd.to_numeric(india_df[india_df.columns[11]], errors='coerce') - 1) / 9
    india_df['Country'] = 'India'

    romania_df['AI_Knowledge_Normalized'] = (pd.to_numeric(romania_df[romania_df.columns[0]], errors='coerce') - 1) / 4
    romania_df['AI_Usage_Normalized'] = (pd.to_numeric(romania_df[romania_df.columns[2]], errors='coerce') - 1) / 4
    romania_df['Country'] = 'Rumania'

    turkey_knowledge_map = {'No knowledge': 0, 'Little knowledge': 1/3, 'Moderate knowledge': 2/3, 'High knowledge': 1}
    turkey_df['AI_Knowledge_Normalized'] = turkey_df[turkey_df.columns[5]].map(turkey_knowledge_map)
    turkey_df['Country'] = 'Turquía'

    combined_frequency_df = pd.concat([bangladesh_df[['Country', 'AI_Usage_Normalized']], romania_df[['Country', 'AI_Usage_Normalized']], india_df[['Country', 'AI_Usage_Normalized']]], ignore_index=True)
    combined_knowledge_df = pd.concat([turkey_df[['Country', 'AI_Knowledge_Normalized']], romania_df[['Country', 'AI_Knowledge_Normalized']], india_df[['Country', 'AI_Knowledge_Normalized']]], ignore_index=True)
    
    return combined_frequency_df, combined_knowledge_df, all_dfs

frequency_df, knowledge_df, original_dfs = load_and_prepare_data()

if frequency_df is not None and knowledge_df is not None:
    st.header('Comparación General Normalizada')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Frecuencia Promedio de Uso de IA')
        fig1, ax1 = plt.subplots()
        sns.barplot(data=frequency_df, x='Country', y='AI_Usage_Normalized', hue='Country', estimator='mean', ax=ax1, palette="viridis", errorbar=None, legend=False)
        st.pyplot(fig1)

    with col2:
        st.subheader('Nivel Promedio de Conocimiento de IA')
        fig2, ax2 = plt.subplots()
        sns.barplot(data=knowledge_df, x='Country', y='AI_Knowledge_Normalized', hue='Country', estimator='mean', ax=ax2, palette="plasma", errorbar=None, legend=False)
        st.pyplot(fig2)

    st.markdown("---")
    st.header("Explora los Datos Originales")
    selected_country = st.selectbox("Selecciona un país:", list(original_dfs.keys()))
    if selected_country:
        st.dataframe(original_dfs[selected_country])