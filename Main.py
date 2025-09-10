import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Verifica se o usuário está logado
if "usuario_logado" not in st.session_state or not st.session_state.usuario_logado:
    st.warning("Você precisa fazer login antes de acessar esta página.")
    st.stop()

st.set_page_config(page_title="AutoTributo", layout="wide")
st.title("AutoTributo – Leitor de Arquivo SPED")

uploaded_file = st.file_uploader("📤 Envie o arquivo .TXT da Receita", type=["txt"])

if uploaded_file is not None:
    dados = uploaded_file.read().decode("utf-8").splitlines()
    blocos = {"C100": [], "C170": []}
    for linha in dados:
        partes = linha.strip().split("|")
        if len(partes) > 1:
            tipo = partes[1]
            if tipo in blocos:
                blocos[tipo].append(partes)

    df_c100 = pd.DataFrame(blocos["C100"]) if blocos["C100"] else pd.DataFrame()
    df_c170 = pd.DataFrame(blocos["C170"]) if blocos["C170"] else pd.DataFrame()

    df_c100.columns = [
        "REG", "IND_OPER", "IND_EMIT", "COD_PART", "COD_MOD", "COD_SIT", "SER", "NUM_DOC",
        "CHV_NFE", "DT_DOC", "DT_ENT", "VL_DOC", "IND_PGTO", "VL_DESC", "VL_ABAT_NT", "VL_MERC",
        "IND_FRT", "VL_FRT", "VL_SEG", "VL_OUT_DA", "VL_BC_ICMS", "VL_ICMS", "VL_BC_ICMS_ST",
        "VL_ICMS_ST", "VL_IPI", "VL_PIS", "VL_COFINS", "VL_PIS_ST", "VL_COFINS_ST"
    ]
    df_c170.columns = [
        "REG", "NUM_ITEM", "COD_ITEM", "DESCR_COMPL", "QTD", "UNID", "VL_ITEM", "VL_DESC",
        "CFOP", "CST_PIS", "CST_COFINS", "ALIQ_PIS", "ALIQ_COFINS"
    ]

    st.success("Arquivo lido com sucesso!")
    st.subheader("📄 Visualização dos dados")
    st.write("Bloco C100 – Cabeçalhos de NFes")
    st.dataframe(df_c100)
    st.write("Bloco C170 – Itens das NFes")
    st.dataframe(df_c170)

    df_c170["credito_permitido"] = df_c170.apply(
        lambda row: str(row["CFOP"]).startswith(("1", "2", "3")) and
                    str(row["CST_PIS"]) in ["50", "51", "52", "53"] and
                    str(row["CST_COFINS"]) in ["50", "51", "52", "53"] and
                    (float(row["ALIQ_PIS"] or 0) > 0 or float(row["ALIQ_COFINS"] or 0) > 0),
        axis=1
    )

    df_c170["credito_ncm"] = df_c170["COD_ITEM"].astype(str).str.startswith("3004")
    df_c170["valor_credito"] = df_c170.apply(
        lambda row: round(float(row["VL_ITEM"] or 0) * (float(row["ALIQ_PIS"] or 0) + float(row["ALIQ_COFINS"] or 0)) / 100, 2),
        axis=1
    )

    df_credito = df_c170[(df_c170["credito_permitido"]) | (df_c170["credito_ncm"])]
    total_credito = df_credito["valor_credito"].sum()

    st.subheader("💰 Itens com crédito permitido de PIS/COFINS")
    st.metric(label="💸 Crédito Fiscal Estimado", value=f"R$ {total_credito:,.2f}")

    st.subheader("🔍 Filtros Interativos")
    cfop_opcoes = sorted(df_credito["CFOP"].dropna().unique())
    cfop_selecionado = st.multiselect("Filtrar por CFOP", cfop_opcoes)

    cst_opcoes = sorted(df_credito["CST_PIS"].dropna().unique())
    cst_selecionado = st.multiselect("Filtrar por CST PIS", cst_opcoes)

    data_inicio = st.date_input("Data inicial", value=pd.to_datetime("2025-01-01"))
    data_fim = st.date_input("Data final", value=pd.to_datetime("2025-12-31"))

    df_c100["DT_DOC"] = pd.to_datetime(df_c100["DT_DOC"], errors="coerce")
    notas_validas = df_c100[
        (df_c100["DT_DOC"] >= pd.to_datetime(data_inicio)) &
        (df_c100["DT_DOC"] <= pd.to_datetime(data_fim))
    ]["NUM_DOC"].unique()

    df_filtrado = df_credito[df_credito["NUM_ITEM"].isin(notas_validas)]
    if cfop_selecionado:
        df_filtrado = df_filtrado[df_filtrado["CFOP"].isin(cfop_selecionado)]
    if cst_selecionado:
        df_filtrado = df_filtrado[df_filtrado["CST_PIS"].isin(cst_selecionado)]

    st.dataframe(df_filtrado)

    st.subheader("📊 Créditos por CFOP")
    cfop_counts = df_credito["CFOP"].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots()
    cfop_counts.plot(kind='bar', ax=ax, color='teal')
    ax.set_title("CFOPs que mais geram crédito")
    ax.set_xlabel("CFOP")
    ax.set_ylabel("Quantidade de Itens")
    st.pyplot(fig)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_credito.to_excel(writer, sheet_name='Itens com Crédito', index=False)
    st.download_button(
        label="📥 Baixar Excel com os dados",
        data=output.getvalue(),
        file_name="AutoTributo_creditos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
