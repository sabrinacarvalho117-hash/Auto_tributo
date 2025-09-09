import streamlit as st
import streamlit_authenticator as stauth

# Usuários e senhas (exemplo simples)
names = ['Sabrina', 'Equipe Fiscal']
usernames = ['sabrina', 'fiscal']
passwords = ['senha123', 'tributo2025']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'auto_tributo_login', 'abcdef', cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.success(f'Bem-vinda, {name}!')
    st.markdown("Você está autenticada e pode acessar todas as funcionalidades do AutoTributo.")
elif authentication_status is False:
    st.error('Usuário ou senha incorretos.')
elif authentication_status is None:
    st.warning('Por favor, insira suas credenciais.')
