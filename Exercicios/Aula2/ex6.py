# Crie uma função que receba duas tuplas representando pontos (x, y) e retorne a distância euclidiana entre eles.
import math
from collections import namedtuple

ponto = namedtuple("ponto", ["x", "y"])

def dist_euclid(p1, p2):
    distancia = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    return distancia

p1 = ponto(1, 2)
p2 = ponto(4, 6)

euclid = dist_euclid(p1, p2)

print(f"p1 eh: ({p1.x}, {p1.y})")
print(f"p2 eh: ({p2.x}, {p2.y})")
print(f"eucldi eh: {euclid:.2f}")