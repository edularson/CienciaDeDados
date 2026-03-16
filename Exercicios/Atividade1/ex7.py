# Dada uma frase, conte quantas vezes cada palavra aparece e exiba as 3 mais frequentes.

from collections import Counter, defaultdict, OrderedDict, namedtuple

frase = "futebol é um jogo criado na Inglaterra onde no futebol exitem 11 jogadores de cada lado sendo um deles o goleiro que defende o gol"

lista = frase.split()
cont = len(lista)

freq = Counter(lista)


print(f"Numero de palavras: {cont}")
print(f"Numero de letras: {lista}")
print(f"Frequencia de palavras: {freq}")

print(f"3 palavras mais utilizadas: {freq.most_common(3)}")