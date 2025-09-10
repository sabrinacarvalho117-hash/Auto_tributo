import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Verifica se o usuário está logado
if "usuario_logado" not in st.session_state or not st.session_state.usuario_logado:
    st.warning("Você precisa fazer login antes de acessar esta página.")
    st.stop()

st.set_page_config(page_title="AutoTributo", page_icon="📊")
st.title("📊 Sistema AutoTributo")

uploaded_file = st.file_uploader("Envie a planilha de notas fiscais", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Visualização da Tabela")
    st.dataframe(df)

    # Filtros
    cfop_filtrado = st.multiselect("Filtrar por CFOP", options=df["CFOP"].unique())
    if cfop_filtrado:
        df = df[df["CFOP"].isin(cfop_filtrado)]

    # Regras de crédito
    def aplicar_credito(row):
        if row["CFOP"] in [5102, 6102] and row["CST"] == 0:
            return row["Valor"] * 0.09
        elif row["NCM"].startswith("3002"):
            return row["Valor"] * 0.12
        else:
            return 0

    df["Crédito"] = df.apply(aplicar_credito, axis=1)

    st.subheader("Notas com Crédito Aplicado")
    st.dataframe(df)

    # Gráfico
    st.subheader("Distribuição de CFOPs")
    fig, ax = plt.subplots()
    df["CFOP"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    # Exportar
    st.subheader("Exportar com Créditos")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Notas com Crédito")
    st.download_button("📥 Baixar Excel", data=output.getvalue(), file_name="notas_credito.xlsx")
