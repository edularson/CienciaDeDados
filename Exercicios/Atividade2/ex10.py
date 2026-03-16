# Inverta a ordem dos elementos em um array 1D [10, 20, 30, 40], de forma que o resultado seja [40, 30, 20, 10].
import numpy as np

arr = np.array([10, 20, 30, 40])

inverter = np.flip(arr)

print(f"invertendo array \n {inverter}")