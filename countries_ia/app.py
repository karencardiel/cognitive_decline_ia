import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página del Dashboard ---
st.set_page_config(layout="wide")
st.title('📊 Dashboard Comparativo del Uso de IA en la Educación')
st.write("""
Este dashboard presenta un análisis comparativo sobre la frecuencia de uso y el nivel de conocimiento 
de la Inteligencia Artificial entre estudiantes de **Bangladesh, India, Rumania y Turquía**. Los datos se han normalizado para permitir una comparación directa entre países.
""")

st.markdown("---")


# --- Carga y Preparación de Datos ---
@st.cache_data
def load_and_prepare_data():
    try:
        bangladesh_df = pd.read_csv('bangladesh.csv')
        india_df = pd.read_csv('india.csv')
        romania_df = pd.read_csv('rumania.csv')
        turkey_df = pd.read_csv('turkey.csv')
    except FileNotFoundError as e:
        st.error(f"Error: No se encontró el archivo {e.filename}. Asegúrate de que los archivos CSV estén en el mismo directorio que el script.")
        return None, None, {}

    all_dfs = {
        'Bangladesh': bangladesh_df.copy(),
        'India': india_df.copy(),
        'Rumania': romania_df.copy(),
        'Turquía': turkey_df.copy()
    }

    # --- Pre-procesamiento y Normalización ---
    
    # Bangladesh
    usage_col_bd = bangladesh_df.columns[2]
    bangladesh_usage_map = {'Never': 0, 'Occasionally': 0.25, 'Monthly': 0.5, 'Weekly': 0.75, 'Daily': 1}
    bangladesh_df['AI_Usage_Normalized'] = bangladesh_df[usage_col_bd].map(bangladesh_usage_map)
    bangladesh_df['Country'] = 'Bangladesh'

    # India
    usage_col_in = india_df.columns[5]
    knowledge_col_in = india_df.columns[11]
    
    india_df[usage_col_in] = pd.to_numeric(india_df[usage_col_in], errors='coerce')
    india_df[knowledge_col_in] = pd.to_numeric(india_df[knowledge_col_in], errors='coerce')
    
    india_df['AI_Usage_Frequency_Category'] = india_df[usage_col_in].apply(lambda x: 'Low' if x < 1 else ('Medium' if 1 <= x <= 3 else 'High'))
    india_usage_map = {'Low': 0.25, 'Medium': 0.5, 'High': 1}
    india_df['AI_Usage_Normalized'] = india_df['AI_Usage_Frequency_Category'].map(india_usage_map)
    india_df['AI_Knowledge_Normalized'] = (india_df[knowledge_col_in] - 1) / 9
    india_df['Country'] = 'India'

    # Romania
    knowledge_col_ro = romania_df.columns[0]
    usage_col_ro = romania_df.columns[2]
    
    romania_df[knowledge_col_ro] = pd.to_numeric(romania_df[knowledge_col_ro], errors='coerce')
    romania_df[usage_col_ro] = pd.to_numeric(romania_df[usage_col_ro], errors='coerce')

    romania_df['AI_Knowledge_Normalized'] = (romania_df[knowledge_col_ro] - 1) / 4
    romania_df['AI_Usage_Normalized'] = (romania_df[usage_col_ro] - 1) / 4
    romania_df['Country'] = 'Rumania'

    # Turkey
    knowledge_col_tr = turkey_df.columns[5]
    turkey_knowledge_map = {'No knowledge': 0, 'Little knowledge': 1/3, 'Moderate knowledge': 2/3, 'High knowledge': 1}
    turkey_df['AI_Knowledge_Normalized'] = turkey_df[knowledge_col_tr].map(turkey_knowledge_map)
    turkey_df['Country'] = 'Turquía'

    # --- Combinación de Datos para Gráficos ---
    combined_frequency_df = pd.concat([
        bangladesh_df[['Country', 'AI_Usage_Normalized']],
        romania_df[['Country', 'AI_Usage_Normalized']],
        india_df[['Country', 'AI_Usage_Normalized']]
    ], ignore_index=True)

    combined_knowledge_df = pd.concat([
        turkey_df[['Country', 'AI_Knowledge_Normalized']],
        romania_df[['Country', 'AI_Knowledge_Normalized']],
        india_df[['Country', 'AI_Knowledge_Normalized']]
    ], ignore_index=True)

    return combined_frequency_df, combined_knowledge_df, all_dfs

frequency_df, knowledge_df, original_dfs = load_and_prepare_data()

if frequency_df is not None and knowledge_df is not None:
    st.header('Comparación General Normalizada')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Frecuencia Promedio de Uso de IA')
        fig1, ax1 = plt.subplots()
        sns.barplot(data=frequency_df, x='Country', y='AI_Usage_Normalized', hue='Country', estimator='mean', ax=ax1, palette="viridis", errorbar=None, legend=False)
        ax1.set_title('Promedio de Frecuencia de Uso de IA por País')
        ax1.set_xlabel('País')
        ax1.set_ylabel('Frecuencia Normalizada (0 a 1)')
        ax1.set_ylim(0, 1)
        st.pyplot(fig1)

    with col2:
        st.subheader('Nivel Promedio de Conocimiento de IA')
        fig2, ax2 = plt.subplots()
        sns.barplot(data=knowledge_df, x='Country', y='AI_Knowledge_Normalized', hue='Country', estimator='mean', ax=ax2, palette="plasma", errorbar=None, legend=False)
        ax2.set_title('Promedio de Nivel de Conocimiento de IA por País')
        ax2.set_xlabel('País')
        ax2.set_ylabel('Conocimiento Normalizado (0 a 1)')
        ax2.set_ylim(0, 1)
        st.pyplot(fig2)

    st.markdown("---")

    st.header("Explora los Datos Originales")
    selected_country = st.selectbox("Selecciona un país para ver sus datos crudos:", list(original_dfs.keys()))
    if selected_country:
        st.dataframe(original_dfs[selected_country])
else:
    st.warning("La carga de datos falló. Por favor, revisa los errores mencionados arriba.")