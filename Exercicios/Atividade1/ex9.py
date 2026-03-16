# Crie uma classe Produto com nome, preço e estoque. Implemente métodos para vender, repor estoque e exibir informações.

class Produto():
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        
    def vender(self, quantidade):
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            print(f"venda de {quantidade} {self.nome}")
        else:
            print(f"n tem estoque")
        
    def repor(self, quantidade):
        self.estoque += quantidade
        print(f"{quantidade} adicionadas no estoque")
        
    def exibir(self):
        print(f"Infos de produto")
        print(f"nome: {self.nome}")
        print(f"preco: R$ {self.preco:.2f}")
        print(f"estoque: {self.estoque}")

produto = Produto("chuteira", 500, 3)
produto.exibir()
produto.vender(2)
produto.exibir()
produto.repor(10)
produto.exibir()

