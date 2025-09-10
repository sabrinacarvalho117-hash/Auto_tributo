import streamlit as st

st.set_page_config(page_title="Login", page_icon="🔐")
st.title("🔐 Login")

# Carregar e-mails aprovados
try:
    with open("aprovados.txt", "r") as f:
        emails_autorizados = [linha.strip() for linha in f if linha.strip()]
except FileNotFoundError:
    emails_autorizados = []

# Campo de entrada
email = st.text_input("Digite seu e-mail para acessar")

# Botão de login
if st.button("Entrar"):
    if email:
        if email in emails_autorizados:
            st.success("Acesso liberado! Bem-vindo ao AutoTributo.")
        else:
            st.error("E-mail não autorizado. Solicite acesso na página de Cadastro.")
    else:
        st.warning("Digite seu e-mail para continuar.")
