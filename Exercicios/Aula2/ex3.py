# Dada uma lista de notas de alunos, calcule e exiba a média, a maior e a menor nota.

notas = [6, 8, 7, 9, 10, 4, 5]

notas.sort()

media = sum(notas) / len(notas)

maior_nota = notas[-1]
menor_nota = notas[0]

print(f"Maior nota: {maior_nota}")
print(f"Menor nota: {menor_nota}")
print(f"Media: {media}")