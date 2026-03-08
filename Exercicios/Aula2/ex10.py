# Crie uma classe base Veiculo e duas subclasses: Carro e Moto. Cada uma deve sobrescrever o método tipo_habilitacao().

class Veiculo:
    def __init__(self, nome):
        self.nome = nome
        
    def tipo_habilitacao(self):
        return "Geral"

class Carro(Veiculo):
    def tipo_habilitacao(self):
        return "eh carro"

class Moto(Veiculo):
    def tipo_habilitacao(self):
        return "eh moto"

carro = Carro("hrv")
moto = Moto("hornet")

print(f"{carro.nome}: {carro.tipo_habilitacao()}")
print(f"{moto.nome}: {moto.tipo_habilitacao()}")
        