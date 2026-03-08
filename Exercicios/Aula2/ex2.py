# Crie uma lista com 5 itens. Adicione 2 itens, remova 1, ordene e exiba o resultado final.

futebol = ["bola", "jogador", "juiz", "gol", "escanteio"]
futebol.append("impedimento")
futebol.append("falta")
print(futebol)
print("--------------------------------------------")
futebol.pop(0)
futebol.sort()
print(futebol)