import streamlit as st
import streamlit_authenticator as stauth

# 🔐 Lista de usuários autorizados
names = ['Sabrina']
usernames = ['sabrina']
passwords = ['12345']  # precisa ser uma lista de strings

# 🔒 Gera os hashes seguros
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
name, authentication_status, username = authenticator.login('Login', 'main')

# ✅ Se login for bem-sucedido
if authentication_status:
    st.success(f'Bem-vinda, {name}!')
    st.markdown("Você está autenticada e pode acessar todas as funcionalidades do AutoTributo.")

# ❌ Se login falhar
elif authentication_status is False:
    st.error('Usuário ou senha incorretos.')

# ⚠️ Se ainda não logou
elif authentication_status is None:
    st.warning('Por favor, insira suas credenciais.')
