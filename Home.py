import streamlit as st

st.set_page_config(page_title="AutoTributo", page_icon="💼", layout="centered")

st.title("💼 AutoTributo")
st.subheader("Solução inteligente para análise fiscal de arquivos SPED")

st.markdown("""
AutoTributo é uma ferramenta que automatiza a leitura, análise e extração de créditos fiscais de arquivos SPED. Ideal para contadores, analistas fiscais e empresas que querem otimizar tempo e garantir conformidade tributária.

### 🚀 Funcionalidades:
- Leitura automática dos blocos C100 e C170
- Aplicação de regras fiscais de PIS/COFINS
- Cálculo de crédito estimado
- Filtros interativos por CFOP, CST e período
- Exportação em Excel, TXT e CSV
- Visualização de notas fiscais com crédito
- Gráficos e relatórios dinâmicos

### 🔐 Segurança:
- Autenticação por usuário
- Controle de acesso por cliente ou equipe

### 📦 Integração:
- Exportação compatível com sistemas contábeis (Domínio, Alterdata, Fortes)
- API pronta para integração com ERPs

### 📞 Contato:
Para licenciamento, integração ou suporte, envie um e-mail para: **contato@autotributo.com.br**
""")

