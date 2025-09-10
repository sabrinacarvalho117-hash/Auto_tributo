import streamlit as st
import urllib.parse

st.set_page_config(page_title="Aprovar Acesso", page_icon="✅")
st.title("✅ Aprovação Automática")

# Captura segura do parâmetro da URL
query_params = st.query_params
email = query_params.get("email", [None])[0]

if email:
    email = urllib.parse.unquote(email)

    try:
        with open("aprovados.txt", "r") as f:
            aprovados = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        aprovados = []

    if email in aprovados:
        st.info(f"O e-mail {email} já está aprovado.")
    else:
        with open("aprovados.txt", "a") as f:
            f.write(email + "\n")
        st.success(f"E-mail {email} aprovado com sucesso!")
else:
    st.warning("Nenhum e-mail foi fornecido para aprovação.")
