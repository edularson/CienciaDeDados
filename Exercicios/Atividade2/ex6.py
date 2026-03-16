# Usando a matriz aleatória do exercício anterior, calcule a soma de todos os elementos em cada coluna.
import numpy as np

matriz = np.random.randint(1,100,(5,5))

print("matriz 5x5 \n", matriz)

print(f"Soma: {matriz.sum()}")