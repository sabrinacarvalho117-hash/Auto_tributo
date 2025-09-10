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
        # Salvar e-mail diretamente como aprovado
        try:
            with open("aprovados.txt", "a") as f:
                f.write(email.strip() + "\n")
        except Exception as e:
            st.error("Erro ao salvar e-mail. Verifique permissões de escrita.")

        # Criar mensagem de e-mail
        msg = EmailMessage()
        msg['Subject'] = 'Solicitação de Permissão - AutoTributo'
        msg['From'] = 'autotributo098@gmail.com'
        msg['To'] = 'sabrinacarvalho117@gmail.com'
        msg.set_content(
            f"Um usuário solicitou acesso ao AutoTributo.\n\n"
            f"E-mail: {email}\n\n"
            f"O e-mail foi aprovado automaticamente e já pode acessar o sistema."
        )

        # Enviar e-mail
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('autotributo098@gmail.com', 'smvmxdncsdprzwqi')
                smtp.send_message(msg)
            st.success("Solicitação enviada e e-mail aprovado com sucesso!")
        except Exception as e:
            st.error("Erro ao enviar e-mail. Verifique as configurações.")
    else:
        st.warning("Digite seu e-mail antes de solicitar.")
