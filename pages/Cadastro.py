import streamlit as st
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Cadastro", page_icon="📝")
st.title("📝 Solicitação de Acesso")

# Campo de entrada
email = st.text_input("Digite seu e-mail")

# Botão de envio
if st.button("Solicitar permissão"):
    if email:
        # Criar mensagem de e-mail
        msg = EmailMessage()
        msg['Subject'] = 'Solicitação de Permissão - AutoTributo'
        msg['From'] = 'autotributo098@gmail.com'
        msg['To'] = 'sabrinacarvalho117@gmail.com'
        msg.set_content(f"""
        Um usuário solicitou acesso ao AutoTributo.

        E-mail: {email}

        Você pode aprovar ou negar manualmente.
        """)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('autotributo098@gmail.com', 'smvmxdncsdprzwqi')  # sua senha de app
                smtp.send_message(msg)
            st.success("Solicitação enviada! Aguarde aprovação por e-mail.")
        except Exception as e:
            st.error("Erro ao enviar solicitação. Verifique as configurações.")
    else:
        st.warning("Digite seu e-mail antes de solicitar.")
# Salvar e-mail em arquivo de solicitações
with open("solicitacoes.txt", "a") as f:
    f.write(email + "\n")
