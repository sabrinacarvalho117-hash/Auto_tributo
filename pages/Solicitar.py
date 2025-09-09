import streamlit as st
import smtplib
from email.mime.text import MIMEText

st.title("📬 Solicitar Acesso ao AutoTributo")

# Formulário
nome = st.text_input("Seu nome completo")
email_usuario = st.text_input("Seu e-mail")
motivo = st.text_area("Por que você deseja acessar o AutoTributo?")
botao = st.button("Solicitar acesso")

# Envio de e-mail
if botao:
    if not nome or not email_usuario or not motivo:
        st.warning("Por favor, preencha todos os campos antes de enviar.")
    else:
        corpo = f"""
        Novo pedido de acesso ao AutoTributo:

        Nome: {nome}
        E-mail: {email_usuario}
        Motivo: {motivo}
        """

        msg = MIMEText(corpo)
        msg['Subject'] = "Solicitação de acesso ao AutoTributo"
        msg['From'] = "sabrinacarvalho117@gmail.com"
        msg['To'] = "sabrinacarvalho117@gmail.com"

        try:
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login("sabrinacarvalho117@gmail.com", "rrxxhgtdfddacvcx")
            servidor.sendmail(msg['From'], [msg['To']], msg.as_string())
            servidor.quit()
            st.success("Solicitação enviada com sucesso! Você será notificada por e-mail.")
        except Exception as e:
            st.error(f"Erro ao enviar e-mail: {e}")
