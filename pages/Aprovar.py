import streamlit as st

st.set_page_config(page_title="Aprovar Acesso", page_icon="✅")
st.title("✅ Aprovação de Acesso")

# Carregar solicitações
try:
    with open("solicitacoes.txt", "r") as f:
        solicitacoes = list(set([linha.strip() for linha in f if linha.strip()]))
except FileNotFoundError:
    solicitacoes = []

# Carregar aprovados
try:
    with open("aprovados.txt", "r") as f:
        aprovados = set([linha.strip() for linha in f if linha.strip()])
except FileNotFoundError:
    aprovados = set()

# Mostrar solicitações pendentes
pendentes = [email for email in solicitacoes if email not in aprovados]

if pendentes:
    for email in pendentes:
        col1, col2 = st.columns([3, 1])
        col1.write(email)
        if col2.button("Aprovar", key=email):
            with open("aprovados.txt", "a") as f:
                f.write(email + "\n")
            st.success(f"{email} aprovado!")
else:
    st.info("Nenhuma solicitação pendente.")
