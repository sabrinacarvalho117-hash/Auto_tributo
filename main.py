import streamlit as st

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

# Interface Streamlit
st.set_page_config(page_title="AutoTributo", layout="wide")
st.title("AutoTributo – Leitor de Arquivo SPED")


    return blocos
# Interface Streamlit
st.set_page_config(page_title="AutoTributo", layout="wide")
st.title("AutoTributo – Leitor de Arquivo SPED")

uploaded_file = st.file_uploader("📤 Envie o arquivo .TXT da Receita", type=["txt"])

if uploaded_file is not None:
    dados = ler_arquivo_sped(uploaded_file)
    st.success("Arquivo lido com sucesso!")
    import pandas as pd
import io

# Transformar blocos em DataFrames
dados = ler_arquivo_sped(uploaded_file)
df_c100 = pd.DataFrame(dados["C100"]) if dados["C100"] else pd.DataFrame()
df_c170 = pd.DataFrame(dados["C170"]) if dados["C170"] else pd.DataFrame()

st.subheader("📄 Visualização dos dados")

st.write("Bloco C100 – Cabeçalhos de NFes")
st.dataframe(df_c100)

st.write("Bloco C170 – Itens das NFes")
st.dataframe(df_c170)

# Função para gerar Excel
def gerar_excel(df1, df2):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='C100', index=False)
        df2.to_excel(writer, sheet_name='C170', index=False)
    return output.getvalue()

# Botão de download
    excel_bytes = gerar_excel(df_c100, df_c170)
    st.download_button(
        label="📥 Baixar Excel com os dados",
        data=excel_bytes,
        file_name="AutoTributo_dados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.write(f"🔹 Notas fiscais encontradas (C100): {len(dados['C100'])}")
    st.write(f"🔹 Itens de nota (C170): {len(dados['C170'])}")

    if st.checkbox("Mostrar blocos C100"):
        st.write(dados["C100"])

    if st.checkbox("Mostrar blocos C170"):
        st.write(dados["C170"])











