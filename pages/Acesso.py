import streamlit as st
import urllib.parse

st.set_page_config(page_title="Acesso", page_icon="🔐")
st.title("🔐 Login ou Cadastro")

email = st.text_input("Digite seu e-mail")

if st.button("Entrar"):
    if email:
        email = email.strip()

        try:
            with open("aprovados.txt", "r") as f:
                aprovados = [linha.strip() for linha in f if linha.strip()]
        except FileNotFoundError:
            aprovados = []

        if email in aprovados:
            st.session_state.usuario_logado = True
            st.success("Login aprovado! Vá para a página principal.")
            st.page_link("main.py", label="Ir para o sistema", icon="➡️")
        else:
            with open("aprovados.txt", "a") as f:
                f.write(email + "\n")
            st.warning("Seu e-mail foi enviado para aprovação. Aguarde liberação.")
    else:
        st.warning("Digite seu e-mail antes de continuar.")
