import streamlit as st

def ler_arquivo_sped(uploaded_file):
    blocos = {
        "C100": [],
        "C170": []
    }

    for linha in uploaded_file:
        linha = linha.decode("utf-8").strip()
        partes = linha.split("|")
        if len(partes) > 1:
            tipo_bloco = partes[1]
            if tipo_bloco in blocos:
                blocos[tipo_bloco].append(partes)

    return blocos

# Interface Streamlit
st.set_page_config(page_title="AutoTributo", layout="wide")
st.title("AutoTributo – Leitor de Arquivo SPED")

uploaded_file = st.file_uploader("📤 Envie o arquivo .TXT da Receita", type=["txt"])

if uploaded_file is not None:
    dados = ler_arquivo_sped(uploaded_file)
    st.success("Arquivo lido com sucesso!")

    st.write(f"🔹 Notas fiscais encontradas (C100): {len(dados['C100'])}")
    st.write(f"🔹 Itens de nota (C170): {len(dados['C170'])}")

    if st.checkbox("Mostrar blocos C100"):
        st.write(dados["C100"])

    if st.checkbox("Mostrar blocos C170"):
        st.write(dados["C170"])
