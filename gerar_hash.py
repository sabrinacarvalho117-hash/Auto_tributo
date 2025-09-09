import streamlit_authenticator as stauth

senha = "12345"
hashed_senha = stauth.Hasher([senha]).generate()

print("Hash gerado:")
print(hashed_senha[0])
