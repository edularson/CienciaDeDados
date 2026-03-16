# Encontre o valor máximo em cada linha da matriz aleatória criada no exercício 5.
import numpy as np

matriz = np.random.randint(1,100,(5,5))

print("matriz 5x5 \n", matriz)

print(f"maior valor: {matriz.max()}")