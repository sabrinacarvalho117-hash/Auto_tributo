import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Função para ler o arquivo SPED
def ler_arquivo_sped(uploaded_file):
    blocos = { "C100": [], "C170": [] }
    conteudo = uploaded_file.read().decode("utf-8")
    for linha in conteudo.splitlines():
        partes = linha.strip().split("|")
        if len(partes) > 1:
            tipo_bloco = partes[1]
            if tipo_bloco in blocos:
                blocos[tipo_bloco].append(partes)
    return blocos

# Função para aplicar regras de crédito de PIS/COFINS
def aplicar_regras_credito(df):
    df["credito_permitido"] = False
    for i, row in df.iterrows():
        try:
            cfop = row[8]
            cst_pis = row[9]
            cst_cofins = row[10]
            aliq_pis = float(row[11]) if row[11] else 0
            aliq_cofins = float(row[12]) if row[12] else 0

            if (
                str(cfop).startswith(("1", "2", "3")) and
                str(cst_pis) in ["50", "51", "52", "53"] and
                str(cst_cofins) in ["50", "51", "52", "53"] and
                (aliq_pis > 0 or aliq_cofins > 0)
            ):
                df.at[i, "credito_permitido"] = True
        except Exception:
            continue
    return df

# Função para calcular crédito estimado
def calcular_credito(df):
    df["valor_credito"] = 0.0
    for i, row in df.iterrows():
        try:
            valor_item = float(row[7]) if row[7] else 0
            aliq_pis = float(row[11]) if row[11] else 0
            aliq_cofins = float(row[12]) if row[12] else 0
            credito = valor_item * (aliq_pis + aliq_cofins) / 100
            df.at[i, "valor_credito"] = round(credito, 2)
        except:
            continue
    return df

# Função para gerar Excel
def gerar_excel(df1, df2):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='C100', index=False)
        df2.to_excel(writer, sheet_name='C170', index=False)
    return output.getvalue()

# Função para gerar Excel com crédito
def gerar_excel_credito(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Itens com Crédito', index=False)
    return output.getvalue()

# Função para gerar TXT com os itens que têm crédito permitido
def gerar_txt_credito(df):
    linhas_formatadas = []
    for linha in df.values:
        partes = [str(campo) if campo is not None else "" for campo in linha]
        linha_formatada = "|" + "|".join(partes) + "|"
        linhas_formatadas.append(linha_formatada)
    return "\n".join(linhas_formatadas)

# Interface Streamlit
st.set_page_config(page_title="AutoTributo", layout="wide")
st.title("AutoTributo – Leitor de Arquivo SPED")

uploaded_file = st.file_uploader("📤 Envie o arquivo .TXT da Receita", type=["txt"])

if uploaded_file is not None:
    dados = ler_arquivo_sped(uploaded_file)

    df_c100 = pd.DataFrame(dados["C100"]) if dados["C100"] else pd.DataFrame()
    df_c170 = pd.DataFrame(dados["C170"]) if dados["C170"] else pd.DataFrame()

    st.success("Arquivo lido com sucesso!")
    st.subheader("📄 Visualização dos dados")

    st.write("Bloco C100 – Cabeçalhos de NFes")
    st.dataframe(df_c100)

    st.write("Bloco C170 – Itens das NFes")
    st.dataframe(df_c170)

    excel_bytes = gerar_excel(df_c100, df_c170)
    st.download_button(
        label="📥 Baixar Excel com os dados",
        data=excel_bytes,
        file_name="AutoTributo_dados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Aplicar regras de crédito
    df_c170 = aplicar_regras_credito(df_c170)

    # Filtrar itens com crédito permitido
    if "credito_permitido" in df_c170.columns:
        df_credito = df_c170[df_c170["credito_permitido"] == True]
        df_credito = calcular_credito(df_credito)
        total_credito = df_credito["valor_credito"].sum()

        st.subheader("💰 Itens com crédito permitido de PIS/COFINS")
        st.metric(label="💸 Crédito Fiscal Estimado (PIS + COFINS)", value=f"R$ {total_credito:,.2f}")

        # Filtros interativos
        st.subheader("🔍 Filtros Interativos")
        cfop_opcoes = sorted(df_credito[8].dropna().unique())
        cfop_selecionado = st.multiselect("Filtrar por CFOP", cfop_opcoes)

        cst_opcoes = sorted(df_credito[9].dropna().unique())
        cst_selecionado = st.multiselect("Filtrar por CST PIS", cst_opcoes)

        df_filtrado = df_credito.copy()
        if cfop_selecionado:
            df_filtrado = df_filtrado[df_filtrado[8].isin(cfop_selecionado)]
        if cst_selecionado:
            df_filtrado = df_filtrado[df_filtrado[9].isin(cst_selecionado)]

        st.dataframe(df_filtrado)

        # Gráfico de CFOPs
        st.subheader("📊 Créditos por CFOP")
        if not df_credito.empty and 8 in df_credito.columns:
            cfop_counts = df_credito[8].value_counts().sort_values(ascending=False)
            fig, ax = plt.subplots()
            cfop_counts.plot(kind='bar', ax=ax, color='teal')
            ax.set_title("CFOPs que mais geram crédito")
            ax.set_xlabel("CFOP")
            ax.set_ylabel("Quantidade de Itens")
            st.pyplot(fig)
        else:
            st.warning("Nenhum CFOP encontrado para gerar o gráfico.")

        # Notas fiscais que geraram crédito
        st.subheader("📑 Notas fiscais com itens que geram crédito")
        notas_com_credito = df_credito[2].unique()
        df_notas_com_credito = df_c100[df_c100[2].isin(notas_com_credito)]
        st.dataframe(df_notas_com_credito)

        # Download TXT e Excel dos itens com crédito
        txt_credito = gerar_txt_credito(df_credito)
        st.download_button(
            label="📄 Baixar TXT com itens que geram crédito",
            data=txt_credito,
            file_name="AutoTributo_credito.txt",
            mime="text/plain"
        )

        excel_credito = gerar_excel_credito(df_credito)
        st.download_button(
            label="📥 Baixar Excel com itens que geram crédito",
            data=excel_credito,
            file_name="AutoTributo_credito.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )












