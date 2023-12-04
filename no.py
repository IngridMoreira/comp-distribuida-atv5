class No:
    def __init__(self, id, recursos):
        self.id = id
        self.recursos = recursos
        self.vizinhos = []
        self.requisicoes_recebidas = []

    def tem_recurso(self, recurso_alvo):
        return recurso_alvo in self.recursos

    def adiciona_requisicao_recebida(self, resource_id):
        self.requisicoes_recebidas.append(resource_id)

    def requisicao_ja_recebida(self, resource_id):
        return resource_id in self.requisicoes_recebidas
