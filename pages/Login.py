import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Carregar config.yaml
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Inicializar autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Tela de login
name, authentication_status, username = authenticator.login("Login", "main")

# Verificar status
if authentication_status:
    st.success(f"Bem-vinda, {name}!")
    st.write("Você está logada no AutoTributo.")
elif authentication_status is False:
    st.error("Usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, insira suas credenciais.")
