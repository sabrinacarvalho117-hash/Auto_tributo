import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Carrega o arquivo de configuração
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Cria o autenticador
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Login
authenticator.login('main')

# Verifica status
if st.session_state["authentication_status"]:
    st.success(f"Bem-vinda, {st.session_state['name']}!")
elif st.session_state["authentication_status"] is False:
    st.error("Usuário ou senha incorretos.")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, insira suas credenciais.")
