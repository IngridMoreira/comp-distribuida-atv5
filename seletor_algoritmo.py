class SeletorAlgoritmo:
    def __init__(self, algoritmos):
        self.algoritmos = algoritmos
        self.algoritmo_selecionado = algoritmos[0]

    def definir_algoritmo(self, rotulo):
        self.algoritmo_selecionado = rotulo

    def obter_algoritmo_selecionado(self):
        return self.algoritmo_selecionado
