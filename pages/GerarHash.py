import streamlit as st
import streamlit_authenticator as stauth

st.title("🔐 Gerador de Hash de Senha")

# Campo para digitar a senha
senha = st.text_input("Digite a senha que deseja criptografar", type="password")

# Botão para gerar o hash
if st.button("Gerar hash"):
    if senha:
        hashed_senha = stauth.Hasher([senha]).generate()
        st.success("Hash gerado com sucesso!")
        st.code(hashed_senha[0], language="yaml")
    else:
        st.warning("Por favor, digite uma senha antes de gerar o hash.")
