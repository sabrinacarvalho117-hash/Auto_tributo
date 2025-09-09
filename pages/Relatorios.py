import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("📊 Relatórios Fiscais")

st.markdown("Visualize os principais indicadores extraídos do SPED.")

# Exemplo de gráfico fictício
cfop_data = pd.Series({"5102": 120, "6108": 80, "1102": 45})
fig, ax = plt.subplots()
cfop_data.plot(kind="bar", ax=ax, color="purple")
ax.set_title("CFOPs com maior volume de crédito")
ax.set_xlabel("CFOP")
ax.set_ylabel("Quantidade de Itens")
st.pyplot(fig)
