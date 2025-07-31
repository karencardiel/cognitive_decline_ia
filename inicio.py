import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de tendencias sobre el impacto de la inteligencia artificial en contextos académicos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para hacer el diseño más profesional
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-info {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>Dashboard de tendencias sobre el impacto de la inteligencia artificial en contextos académicos</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar mejorado
with st.sidebar:
    st.success("✅ Selecciona un dashboard para continuar.")

# Contenido principal
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="dashboard-card">
        <div class="feature-icon">📈</div>
        <h3>Análisis SAT</h3>
        <p><strong>Análisis de Calificaciones Académicas</strong></p>
        <p>Análisis avanzado de los puntajes SAT (Scholastic Assessment Test) para examinar el rendimiento académico estudiantil y las tendencias en las pruebas estandarizadas de admisión universitaria.</p>
        <ul>
            <li>📊 Análisis de puntajes SAT</li>
            <li>🔍 Patrones de rendimiento</li>
            <li>📋 Comparativas por sección</li>
            <li>⚡ Tendencias temporales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="dashboard-card">
        <div class="feature-icon">💬</div>
        <h3>Análisis de Comentarios</h3>
        <p><strong>Análisis de Sentimientos y Habilidades Cognitivas</strong></p>
        <p>Explore los sentimientos y las habilidades cognitivas mencionadas en comentarios de videos de YouTube sobre Inteligencia Artificial usando técnicas avanzadas de NLP.</p>
        <ul>
            <li>🎭 Análisis de sentimientos</li>
            <li>🧠 Detección de habilidades cognitivas</li>
            <li>📊 Visualizaciones interactivas</li>
            <li>📈 Tendencias temporales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="dashboard-card">
        <div class="feature-icon">🌍</div>
        <h3>Comparativa Países</h3>
        <p><strong>Análisis Global de Adopción de IA</strong></p>
        <p>Compare la frecuencia de uso y el nivel de conocimiento sobre Inteligencia Artificial entre estudiantes de diferentes países con visualizaciones geográficas interactivas.</p>
        <ul>
            <li>🗺️ Mapas interactivos</li>
            <li>📊 Comparativas estadísticas</li>
            <li>🎓 Análisis por nivel educativo</li>
            <li>📈 Métricas de adopción</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)