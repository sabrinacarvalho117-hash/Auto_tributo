def ler_arquivo_txt(conteudo_bytes):
    conteudo = conteudo_bytes.decode("utf-8")
    linhas = conteudo.splitlines()
    return linhas
