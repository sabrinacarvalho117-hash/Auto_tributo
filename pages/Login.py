import streamlit as st

st.set_page_config(page_title="Login", page_icon="🔐")
st.title("🔐 Login")

# Lista de e-mails autorizados
emails_autorizados = [
    "usuario1@email.com",
    "usuario2@email.com",
    "sabrinacarvalho117@gmail.com"
]

# Campo de entrada
email = st.text_input("Digite seu e-mail para acessar")

# Botão de login
if st.button("Entrar"):
    if email:
        if email in emails_autorizados:
            st.success("Acesso liberado! Bem-vindo ao AutoTributo.")
            # Aqui você pode redirecionar ou mostrar conteúdo exclusivo
        else:
            st.error("E-mail não autorizado. Solicite acesso na página de Cadastro.")
    else:
        st.warning("Digite seu e-mail para continuar.")
