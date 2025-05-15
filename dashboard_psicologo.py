
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

# Configuración
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Dashboard Terapéutico con Formulario")
st.markdown("Visualización + carga manual de sesiones. (versión XLSX corregida)")

# Cargar datos existentes
xlsx_file = "datos_psicologos_pacientes.xlsx"
if os.path.exists(xlsx_file):
    df = pd.read_excel(xlsx_file, engine="openpyxl")
else:
    df = pd.DataFrame(columns=[
        "Paciente", "Fecha", "Estado emocional (1-10)",
        "Tema trabajado", "Compromisos asumidos", "Cumplido"
    ])

# Corregir formato de fechas
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
df = df.dropna(subset=["Fecha"])  # Elimina filas sin fecha válida

# Selector de paciente
pacientes = df["Paciente"].unique().tolist()
nuevo_paciente = st.checkbox("Agregar nuevo paciente")
if nuevo_paciente:
    seleccion = st.text_input("Nombre del nuevo paciente")
else:
    seleccion = st.selectbox("Seleccionar paciente", pacientes)

# Formulario para nueva sesión
with st.expander("➕ Registrar nueva sesión"):
    with st.form("formulario_sesion"):
        fecha = st.date_input("Fecha de sesión", value=date.today())
        estado = st.slider("Estado emocional (1-10)", 1, 10, 5)
        tema = st.text_input("Tema trabajado")
        compromiso = st.text_input("Compromisos asumidos")
        cumplido = st.selectbox("¿Cumplido?", ["Sí", "No", "En proceso"])
        submit = st.form_submit_button("Guardar sesión")

        if submit and seleccion:
            nueva_fila = pd.DataFrame([{
                "Paciente": seleccion,
                "Fecha": pd.to_datetime(fecha),
                "Estado emocional (1-10)": estado,
                "Tema trabajado": tema,
                "Compromisos asumidos": compromiso,
                "Cumplido": cumplido
            }])
            df = pd.concat([df, nueva_fila], ignore_index=True)
            df.to_excel(xlsx_file, index=False, engine="openpyxl")
            st.success("✅ Sesión registrada correctamente.")

# Mostrar dashboard si hay datos
if seleccion in df["Paciente"].unique():
    df_filtrado = df[df["Paciente"] == seleccion].sort_values("Fecha")

    col1, col2, col3 = st.columns(3)
    col1.metric("Sesiones", len(df_filtrado))
    col2.metric("Promedio emocional", round(df_filtrado["Estado emocional (1-10)"].mean(), 2))
    col3.metric("Compromisos cumplidos", f"{df_filtrado['Cumplido'].value_counts().get('Sí', 0)} / {len(df_filtrado)}")

    st.markdown("---")
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.subheader("📈 Evolución emocional")
        fig = px.line(df_filtrado, x="Fecha", y="Estado emocional (1-10)", markers=True)
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_der:
        st.subheader("📋 Sesiones")
        st.dataframe(df_filtrado[["Fecha", "Tema trabajado", "Cumplido"]], use_container_width=True)

    st.markdown("---")
    ultima = df_filtrado.iloc[-1]
    st.markdown("### 🧠 Última sesión")
    st.markdown(f"🗓️ Fecha: **{ultima['Fecha'].strftime('%Y-%m-%d')}**")
    st.markdown(f"💬 Tema: _{ultima['Tema trabajado']}_")
    st.markdown(f"📌 Compromiso: {ultima['Compromisos asumidos']}")
    st.markdown(f"✅ Cumplido: **{ultima['Cumplido']}**")
