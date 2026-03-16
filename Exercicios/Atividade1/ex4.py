# Use list comprehension para gerar uma lista com os números ímpares de 1 a 20.

impares = [n for n in range(1, 20) if n % 2 != 0]
print(impares)