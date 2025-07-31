
# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy.stats import ttest_ind, zscore


# Título
st.title("📊 Dashboard de Análisis Puntuaciones de exámenes de admisión")

# Carga de datos
path_2021 = os.path.join("data", "clean", "2021-2022.csv")
path_2023 = os.path.join("data", "clean", "2023-2024.csv")

df_2021 = pd.read_csv(path_2021)
df_2023 = pd.read_csv(path_2023)

# Limpieza básica
cols = ["SAT_AVG_ALL", "SATVR25", "SATVR75", "SATMT25", "SATMT75"]
df_2021[cols] = df_2021[cols].apply(pd.to_numeric, errors="coerce")
df_2023[cols] = df_2023[cols].apply(pd.to_numeric, errors="coerce")



t_stat, p_value = ttest_ind(df_2021["SAT_AVG_ALL"], df_2023["SAT_AVG_ALL"], equal_var=True)

# Cohen's d
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx - 1)*np.std(x, ddof=1)**2 + (ny - 1)*np.std(y, ddof=1)**2) / (nx + ny - 2))
    return (np.mean(x) - np.mean(y)) / pooled_std

d = cohens_d(df_2021["SAT_AVG_ALL"], df_2023["SAT_AVG_ALL"])

# --- Layout con columnas ---
st.subheader("🧪 Prueba de Hipótesis: Comparación SAT_AVG_ALL (2021–2022 vs 2023–2024)")

col_spacer,col1, col2 = st.columns([0.25,1, 1.25])  # KDE más ancho

with col1:
    st.markdown("#### 📊 Resultados Estadísticos")
    st.write(f"• **Estadístico t**: {t_stat:.3f}")
    st.write(f"• **Valor p**: {p_value:.4f}")
    st.write("• **¿Diferencia significativa?**: {}".format("✅ Sí (p < 0.05)" if p_value < 0.05 else "❌ No (p ≥ 0.05)"))
    st.write(f"• **d de Cohen**: {d:.3f}")
    st.write("Hay diferencia estadística pero el tamaño de impacto en la práctica no es significativo.")

with col2:
    # KDE plot
    fig_kde, ax = plt.subplots(figsize=(6, 3))
    sns.kdeplot(df_2021["SAT_AVG_ALL"], label="2021–2022", fill=True, alpha=0.5, ax=ax)
    sns.kdeplot(df_2023["SAT_AVG_ALL"], label="2023–2024", fill=True, alpha=0.5, ax=ax)
    ax.set_title("Distribución de SAT_AVG_ALL por Año (KDE)")
    ax.set_xlabel("Puntaje SAT")
    ax.set_ylabel("Densidad")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig_kde)

# --- Fila inferior con boxplot y barplot ---
col3, col4 = st.columns(2)

# Preparación
df_2021_temp = df_2021.assign(Year="2021–2022")
df_2023_temp = df_2023.assign(Year="2023–2024")
df_box = pd.concat([df_2021_temp, df_2023_temp])

# Boxplot
col_box, col_spacer, col_bar = st.columns([1.2, 0.3, 1.8])  # proporciones: más espacio al barplot

# Preparación
df_2021_temp = df_2021.assign(Year="2021–2022")
df_2023_temp = df_2023.assign(Year="2023–2024")
df_box = pd.concat([df_2021_temp, df_2023_temp])
# Calcular el cambio porcentual por institución
df_merged = pd.merge(
    df_2021[["INSTNM", "SAT_AVG_ALL"]],
    df_2023[["INSTNM", "SAT_AVG_ALL"]],
    on="INSTNM",
    suffixes=("_2021", "_2023")
)

df_merged["%_cambio_SAT"] = (
    (df_merged["SAT_AVG_ALL_2023"] - df_merged["SAT_AVG_ALL_2021"]) / df_merged["SAT_AVG_ALL_2021"]
) * 100

# Seleccionamos top 5 positivos y negativos
top_positive = df_merged.sort_values(by="%_cambio_SAT", ascending=False).head(5)
top_negative = df_merged.sort_values(by="%_cambio_SAT", ascending=True).head(5)

# Unión final
df_barras = pd.concat([top_positive, top_negative]).sort_values(by="%_cambio_SAT")

col_box, col_spacer, col_bar = st.columns([1.2, 0.3, 1.8])  # proporciones: más espacio al barplot

# Boxplot reducido
with col_box:
    fig_box, ax = plt.subplots()
    sns.boxplot(data=df_box, x="Year", y="SAT_AVG_ALL", palette="Set2", ax=ax)
    ax.set_title("Boxplot de SAT_AVG_ALL por Año", fontsize=12)
    ax.set_ylabel("Puntaje SAT")
    ax.grid(True, axis='y', linestyle="--", alpha=0.6)
    st.pyplot(fig_box)

# Espacio vacío en el centro
with col_spacer:
    st.write("")

# Barplot amplio
with col_bar:
    fig_bar, ax = plt.subplots()
    sns.barplot(data=df_barras, x="%_cambio_SAT", y="INSTNM", palette="coolwarm", ax=ax)
    ax.set_title("Top ±5 Cambios % SAT_AVG_ALL por Institución", fontsize=12)
    ax.set_xlabel("Cambio porcentual")
    ax.set_ylabel("Institución")
    ax.axvline(x=0, color="gray", linestyle="--")
    ax.grid(True, axis='x', linestyle="--", alpha=0.6)
    st.pyplot(fig_bar)


import matplotlib.pyplot as plt

# KPIs
kpi_2021 = df_2021["SAT_AVG_ALL"].agg(["mean", "std", "min", "max"]).round(2)
kpi_2023 = df_2023["SAT_AVG_ALL"].agg(["mean", "std", "min", "max"]).round(2)

# Definimos categorías de desempeño
bins = [0, 1000, 1200, 1400, 1500, float("inf")]
labels = ["Bajo", "Básico", "Intermedio", "Alto", "Sobresaliente"]

# Añadimos categoría al DataFrame
df_2021["Desempeño"] = pd.cut(df_2021["SAT_AVG_ALL"], bins=bins, labels=labels)
df_2023["Desempeño"] = pd.cut(df_2023["SAT_AVG_ALL"], bins=bins, labels=labels)

# Conteos para pie charts
desempeno_2021 = df_2021["Desempeño"].value_counts().sort_index()
desempeno_2023 = df_2023["Desempeño"].value_counts().sort_index()

# Layout de 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("#### 🔵 Año 2021–2022")
    st.write(f"• Media: {kpi_2021['mean']}")
    st.write(f"• Desviación estándar: {kpi_2021['std']}")
    st.write(f"• Mínimo: {kpi_2021['min']}")
    st.write(f"• Máximo: {kpi_2021['max']}")

with col2:
    fig1, ax1 = plt.subplots()
    ax1.pie(desempeno_2021, labels=desempeno_2021.index, autopct="%1.1f%%", startangle=140)
    ax1.axis("equal")
    st.pyplot(fig1)

with col3:
    st.markdown("#### 🟢 Año 2023–2024")
    st.write(f"• Media: {kpi_2023['mean']}")
    st.write(f"• Desviación estándar: {kpi_2023['std']}")
    st.write(f"• Mínimo: {kpi_2023['min']}")
    st.write(f"• Máximo: {kpi_2023['max']}")

with col4:
    fig2, ax2 = plt.subplots()
    ax2.pie(desempeno_2023, labels=desempeno_2023.index, autopct="%1.1f%%", startangle=140)
    ax2.axis("equal")
    st.pyplot(fig2)




mean_2021 = df_2021["SAT_AVG_ALL"].mean()
mean_2023 = df_2023["SAT_AVG_ALL"].mean()
pct_change = ((mean_2023 - mean_2021) / mean_2021) * 100

verbal_2021 = (df_2021["SATVR25"] + df_2021["SATVR75"]) / 2
math_2021 = (df_2021["SATMT25"] + df_2021["SATMT75"]) / 2
ratio_2021 = verbal_2021.mean() / math_2021.mean()

verbal_2023 = (df_2023["SATVR25"] + df_2023["SATVR75"]) / 2
math_2023 = (df_2023["SATMT25"] + df_2023["SATMT75"]) / 2
ratio_2023 = verbal_2023.mean() / math_2023.mean()

# Z-score promedio
df_z = pd.concat([
    df_2021.assign(Year="2021–2022"),
    df_2023.assign(Year="2023–2024")
])
df_z["SAT_AVG_ALL_Z"] = zscore(df_z["SAT_AVG_ALL"])
zscore_means = df_z.groupby("Year")["SAT_AVG_ALL_Z"].mean()

# ---------------------------
# Layout en columnas
# ---------------------------

st.subheader("📊 Métricas Complementarias")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📌 Variación % SAT Promedio")
    st.markdown(f"**{pct_change:.2f}%**")

with col2:
    st.markdown("#### 📏 Ratio Verbal/Matemático")
    st.markdown(f"**2021–2022:** {ratio_2021:.3f}  \n**2023–2024:** {ratio_2023:.3f}")

with col3:
    st.markdown("#### ⚖️ Variación de media")
    st.markdown(f"**2023–2024:** {zscore_means['2023–2024']:.3f}")

st.markdown("---")
st.subheader("📊 Interés Global y Publicaciones sobre IA en Educación")

col1,col_spacer, col2 = st.columns([1,0.5,1])

with col1:
    st.markdown("#### 🔎 Tendencias de Búsqueda Simuladas (GTrends)")
    years = np.arange(2018, 2025)
    trends = pd.DataFrame({
        "Año": years,
        "ChatGPT": [0, 0, 0, 0, 25, 75, 90],
        "Gemini": [0, 0, 0, 0, 15, 55, 65],
        "Wikipedia": [30, 35, 40, 38, 42, 45, 48],
        "Sci-Hub": [40, 42, 43, 41, 44, 46, 50],
        "Google Scholar": [20, 25, 30, 40, 50, 55, 60],
    })

    fig, ax = plt.subplots()
    for col in trends.columns[1:]:
        ax.plot(trends["Año"], trends[col], label=col, linewidth=2)

    ax.set_title("Tendencias de Búsqueda (2018–2024)", fontsize=12)
    ax.set_ylabel("Interés relativo (%)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with col2:
    st.markdown("#### 📚 Publicaciones sobre IA en Educación (Simulación)")

    pub_years = np.arange(2018, 2025)
    pub_counts = [50, 60, 75, 110, 200, 320, 460]

    fig2, ax2 = plt.subplots()
    ax2.plot(pub_years, pub_counts, marker='o', linestyle='--', color='purple')
    ax2.set_title("Publicaciones por Año (Simulado)", fontsize=12)
    ax2.set_xlabel("Año")
    ax2.set_ylabel("Cantidad de Publicaciones")
    ax2.grid(True)
    st.pyplot(fig2)

