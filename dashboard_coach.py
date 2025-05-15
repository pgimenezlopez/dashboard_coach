import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Datos simulados
data = {
    "Fecha": ["2025-04-15", "2025-04-22", "2025-04-29"],
    "Estado emocional (1-10)": [5, 6, 7],
    "Compromisos cumplidos (%)": [100, 100, 50]
}
df = pd.DataFrame(data)

# Título
st.title("🌿 Dashboard de Bienestar – Lucía González")
st.markdown("Visualización del progreso emocional y cumplimiento de objetivos.")

st.markdown("---")

# Layout dividido
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Registro de sesiones")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📈 Estado emocional")
    fig, ax = plt.subplots()
    ax.plot(df["Fecha"], df["Estado emocional (1-10)"], marker='o', color="#2ECC71")
    ax.set_ylim(0, 10)
    ax.set_ylabel("Escala 1-10")
    st.pyplot(fig)

st.markdown("---")

# Gráfico de barras al final
st.subheader("✅ Compromisos cumplidos")
st.bar_chart(df.set_index("Fecha")["Compromisos cumplidos (%)"])

# Footer
st.markdown("---")
st.caption("Desarrollado con ❤️ usando Streamlit – Versión demo")
