import streamlit as st
from processador import ler_arquivo_txt

st.set_page_config(page_title="AutoTributo", layout="wide")
st.title("AutoTributo - Leitor de Arquivo da Receita")

arquivo = st.file_uploader("📤 Envie o arquivo .txt da Receita", type="txt")

if arquivo:
    linhas = ler_arquivo_txt(arquivo.read())
    st.subheader("📄 Conteúdo do arquivo:")
    for linha in linhas:
        st.text(linha)
