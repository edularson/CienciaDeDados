import re
from collections import Counter

with open("texto.txt", "r", encoding="utf-8") as f:
    texto = f.read()

palavras = re.findall(r'\b[a-záéíóúãõâêîôûç]+\b', texto.lower())
contagem = Counter(palavras)

for palavra, qtd in contagem.most_common(10):
    print(f"{palavra}: {qtd}")