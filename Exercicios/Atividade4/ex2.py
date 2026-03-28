import csv

categoria_filtro = "Eletrônicos"
precos = []

with open("produtos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for linha in reader:
        if linha["categoria"] == categoria_filtro:
            precos.append(float(linha["preco"]))

if precos:
    media = sum(precos) / len(precos)
    print(f"Preço médio dos {categoria_filtro}: R$ {media:.2f}")
else:
    print("Nenhum produto encontrado nessa categoria.")