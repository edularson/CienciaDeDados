# Crie uma função estatisticas() que aceite qualquer quantidade de números e retorne um dicionário com média, máximo e mínimo.

def estatisticas(*numeros):
    if not numeros:
        return {"media": 0, "maximo": 0, "minimo": 0}

    soma = sum(numeros)
    qtd = len(numeros)
    
    dicionario = {
        "media": soma / qtd,
        "maximo": max(numeros),
        "minimo": min(numeros)
    }
    
    return dicionario

resultado = estatisticas(10, 20, 30, 40, 50)
print(resultado)