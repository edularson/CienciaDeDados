# Dado o array [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], extraia apenas os números ímpares.

import numpy as np

matriz = np.arange(10)

print("matriz com todos os valores",matriz)

impares = matriz[matriz % 2 != 0]
print("matriz impares", impares)