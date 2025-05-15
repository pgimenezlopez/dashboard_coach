
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración visual oculta menú y pie de página
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Título y logo
st.title("🧠 Dashboard Terapéutico")
st.markdown("Visualización del progreso emocional de pacientes a lo largo del proceso terapéutico.")


# Cargar datos desde CSV
#df = pd.read_csv("datos_psicologos_pacientes.csv")
df = pd.read_excel("datos_pacientes.xlsx")

# Selector de paciente
pacientes = df["Paciente"].unique()
seleccion = st.selectbox("Seleccionar paciente", pacientes)

# Filtrar datos
df_filtrado = df[df["Paciente"] == seleccion]

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("Sesiones registradas", len(df_filtrado))
col2.metric("Estado emocional promedio", round(df_filtrado["Estado emocional (1-10)"].mean(), 2))
col3.metric("Compromisos cumplidos", f"{df_filtrado['Cumplido'].value_counts().get('Sí', 0)} / {len(df_filtrado)}")

st.markdown("---")

# Layout de dos columnas
col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.subheader("📈 Evolución emocional")
    fig = px.line(df_filtrado, x="Fecha", y="Estado emocional (1-10)", markers=True,
                  title=f"Evolución emocional de {seleccion}",
                  labels={"Estado emocional (1-10)": "Escala 1–10"})
    fig.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig, use_container_width=True)

with col_der:
    st.subheader("📋 Resumen de sesiones")
    st.dataframe(df_filtrado[["Fecha", "Tema trabajado", "Cumplido"]], use_container_width=True)

st.markdown("---")

# Última sesión
ultima = df_filtrado.sort_values("Fecha").iloc[-1]
st.markdown("### 🧠 Última sesión registrada")
st.markdown(f"🗓️ Fecha: **{ultima['Fecha']}**")
st.markdown(f"💬 Tema trabajado: _{ultima['Tema trabajado']}_")
st.markdown(f"📌 Compromiso: {ultima['Compromisos asumidos']}")
st.markdown(f"✅ Cumplido: **{ultima['Cumplido']}**")

st.markdown("---")
st.caption("Versión 2.1 · Desarrollado por Pablo Giménez · Streamlit + Plotly")
