import streamlit as st
import smtplib
from email.message import EmailMessage

st.title("📝 Solicitação de Cadastro")

email = st.text_input("Digite seu e-mail")
senha = st.text_input("Crie uma senha", type="password")

if st.button("Solicitar acesso"):
    if email and senha:
        msg = EmailMessage()
        msg['Subject'] = 'Solicitação de Cadastro - AutoTributo'
        msg['From'] = 'autotributo@gmail.com'  # precisa ser um e-mail real
        msg['To'] = 'sabrinacarvalho117@gmail.com'
        msg.set_content(f"""
        Novo usuário solicitou acesso ao AutoTributo:

        E-mail: {email}
        Senha: {senha}

        Você pode aprovar manualmente adicionando ao sistema.
        """)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('autotributo@gmail.com', 'SENHA_DO_APP')
                smtp.send_message(msg)
            st.success("Solicitação enviada! Aguarde aprovação por e-mail.")
        except Exception as e:
            st.error("Erro ao enviar e-mail. Verifique as configurações.")
    else:
        st.warning("Preencha todos os campos antes de solicitar.")
