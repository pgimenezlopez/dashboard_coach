
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde CSV
#df = pd.read_csv("datos_psicologos_pacientes.csv")
df = pd.read_excel("datos_pacientes.xlsx")

st.title("🧠 Dashboard de Seguimiento Terapéutico")

# Selector de paciente
pacientes = df["Paciente"].unique()
seleccion = st.selectbox("Seleccionar paciente", pacientes)

# Filtrar datos
df_filtrado = df[df["Paciente"] == seleccion]

# Mostrar tabla
st.subheader("📋 Registro de sesiones")
st.dataframe(df_filtrado, use_container_width=True)

# Gráfico de evolución emocional
st.subheader("📈 Evolución del estado emocional")
fig, ax = plt.subplots()
ax.plot(df_filtrado["Fecha"], df_filtrado["Estado emocional (1-10)"], marker="o", color="#3498db")
ax.set_ylim(0, 10)
ax.set_ylabel("Escala 1–10")
ax.set_xlabel("Fecha")
st.pyplot(fig)

# Cumplimiento de compromisos
st.subheader("✅ Estado de compromisos")
st.write(df_filtrado[["Fecha", "Compromisos asumidos", "Cumplido"]])

st.markdown("---")
st.caption("Demo desarrollada con Streamlit · Pablo Giménez")
