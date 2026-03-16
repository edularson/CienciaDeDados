import numpy as np

np.set_printoptions(precision=2, suppress=True)

matriz = np.random.randint(100, 500, size=(3, 4))

print("matriz aleatoria", matriz)
print("venda total: ", matriz.sum(axis=1))
print("media de vendas de cada dia: ", matriz.mean(axis=0))
print("dias que tiveram mais de 400 vendas: ", matriz[matriz > 400])

