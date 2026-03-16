# No array [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], substitua todos os números ímpares por -1.
import numpy as np

matriz = np.arange(10)

print("matriz com todos os valores",matriz)

matriz[matriz % 2 != 0] = -1
print("matriz impares", matriz)