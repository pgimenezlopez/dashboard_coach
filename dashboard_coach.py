import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard de Progreso - Cliente: Lucía González")

data = {
    "Fecha": ["2025-04-15", "2025-04-22", "2025-04-29"],
    "Estado emocional (1-10)": [5, 6, 7],
    "Compromisos cumplidos (%)": [100, 100, 50]
}
df = pd.DataFrame(data)

st.subheader("📅 Registro de sesiones")
st.dataframe(df)

st.subheader("📈 Estado emocional a lo largo del tiempo")
fig, ax = plt.subplots()
ax.plot(df["Fecha"], df["Estado emocional (1-10)"], marker='o')
ax.set_ylim(0, 10)
st.pyplot(fig)

st.subheader("✅ Cumplimiento de compromisos")
st.bar_chart(df.set_index("Fecha")["Compromisos cumplidos (%)"])
