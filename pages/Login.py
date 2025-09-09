import streamlit as st
import streamlit_authenticator as stauth

# 🔐 Lista de usuários autorizados
names = ['Sabrina']
usernames = ['sabrina']
passwords = ['12345']  # lista de senhas em texto

# ✅ Gera os hashes corretamente (usando lista)
hashed_passwords = stauth.Hasher(passwords).generate()

# 🔐 Configuração do autenticador
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'auto_tributo_login',       # nome do cookie
    'segredo_sabrina',          # chave de assinatura
    cookie_expiry_days=30       # validade do login
)

# 🧑 Login
authenticator.login('Login', 'main')

# 🔍 Verifica status de autenticação
if st.session_state["authentication_status"]:
    st.success(f'Bem-vinda, {st.session_state["name"]}!')
    st.markdown("Você está autenticada e pode acessar todas as funcionalidades do AutoTributo.")

elif st.session_state["authentication_status"] is False:
    st.error('Usuário ou senha incorretos.')

elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, insira suas credenciais.')


