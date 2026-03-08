# Crie um dicionário com pelo menos 3 contatos (nome como chave, telefone como valor). Permita busca pelo nome.

contatos = {
    "Eduardo": "98871-5757",
    "Th Ceron": "91111-2222",
    "Palm": "99999-9999"
}

for nomes in contatos:
    print(nomes)

busca = input("digite o nome que vc quer buscar: ")

if busca in contatos:
    print(f"telefone de {busca} eh: {contatos[busca]}")
else:
    print("n achou.")