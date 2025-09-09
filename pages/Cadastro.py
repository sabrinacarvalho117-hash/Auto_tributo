import streamlit as st
import smtplib
from email.message import EmailMessage

st.title("📝 Cadastro de Novo Usuário")

# Campos de entrada
email = st.text_input("Digite seu e-mail")
senha = st.text_input("Crie uma senha", type="password")

# Botão de envio
if st.button("Solicitar Cadastro"):
    if email and senha:
        # Montar e-mail para Sabrina
        msg = EmailMessage()
        msg['Subject'] = 'Solicitação de Cadastro - AutoTributo'
        msg['From'] = 'autotributo@gmail.com'  # precisa ser um e-mail real
        msg['To'] = 'sabrinacarvalho117@gmail.com'
        msg.set_content(f"""
        Novo usuário solicitou acesso ao AutoTributo:

        E-mail: {email}
        Senha: {senha}

        Para aprovar, acesse o painel de administração ou responda este e-mail.
        """)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('autotributo@gmail.com', 'SENHA_DO_APP')
                smtp.send_message(msg)
            st.success("Solicitação enviada! Aguarde aprovação por e-mail.")
        except Exception as e:
            st.error(f"Erro ao enviar e-mail: {e}")
    else:
        st.warning("Preencha todos os campos antes de solicitar.")
