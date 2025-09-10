import streamlit as st
import smtplib
from email.message import EmailMessage
import urllib.parse

st.set_page_config(page_title="Cadastro", page_icon="📝")
st.title("📝 Solicitação de Acesso")

# Campo de entrada
email = st.text_input("Digite seu e-mail")

# Botão de envio
if st.button("Solicitar permissão"):
    if email:
        # Gerar link de aprovação automática
        email_encoded = urllib.parse.quote(email)
        link_aprovacao = f"https://autotributo.streamlit.app/Aprovar?email={email_encoded}"

        # Criar mensagem de e-mail
        msg = EmailMessage()
        msg['Subject'] = 'Solicitação de Permissão - AutoTributo'
        msg['From'] = 'autotributo098@gmail.com'
        msg['To'] = 'sabrinacarvalho117@gmail.com'
        msg.set_content(
            f"Um usuário solicitou acesso ao AutoTributo.\n\n"
            f"E-mail: {email}\n\n"
            f"Para aprovar automaticamente, clique neste link:\n{link_aprovacao}"
        )

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('autotributo098@gmail.com', 'smvmxdncsdprzwqi')  # sua senha de app
                smtp.send_message(msg)
            st.success("Solicitação enviada! Aguarde aprovação.")
        except Exception as e:
            st.error("Erro ao enviar solicitação. Verifique as configurações.")
    else:
        st.warning("Digite seu e-mail antes de solicitar.")


Para aprovar automaticamente, clique neste link:
{link_aprovacao}
""")
