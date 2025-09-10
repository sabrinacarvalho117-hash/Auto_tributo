import streamlit as st

st.set_page_config(page_title="Acesso", page_icon="🔐")
st.title("🔐 Login ou Cadastro")

email = st.text_input("Digite seu e-mail")

if email:
    email = email.strip()

    # Lista de e-mails aprovados manualmente
    aprovados = ["sabrinacarvalho117@gmail.com"]

    # Tenta carregar e-mails aprovados do arquivo
    try:
        with open("aprovados.txt", "r") as f:
            aprovados += [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        pass

    if email in aprovados:
        st.session_state.usuario_logado = True
        st.success("Login aprovado! Vá para a página principal.")
        st.page_link("Main.py", label="Ir para o sistema", icon="➡️")
    else:
        try:
            with open("aprovados.txt", "a") as f:
                f.write(email + "\n")
        except Exception:
            st.error("Erro ao salvar e-mail para aprovação.")
        st.warning("Seu e-mail foi enviado para aprovação. Aguarde liberação.")
