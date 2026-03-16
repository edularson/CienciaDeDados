# Crie dois arrays 1D, a = np.array([1, 2, 3]) e b = np.array([4, 5, 6]), e concatene-os horizontalmente para formar um único array.
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

juntos = np.hstack((a,b))
print(f"juntando arrays A e B \n {juntos}")