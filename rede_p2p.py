import networkx as nx


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


class RedeP2P:
    def __init__(self):
        self.nos = []
        self.grafo = nx.Graph()

    def adicionar_no(self, no):
        self.nos.append(no)
        self.grafo.add_node(no.id)

    def adicionar_aresta(self, no1, no2):
        no1.vizinhos.append(no2)
        no2.vizinhos.append(no1)
        self.grafo.add_edge(no1.id, no2.id)

    def esta_particionada(self):
        return not nx.is_connected(self.grafo)

    def atende_limites(self, min_vizinhos, max_vizinhos):
        for no in self.nos:
            num_vizinhos = len(no.vizinhos)
            if num_vizinhos < min_vizinhos or num_vizinhos > max_vizinhos:
                return False
        return True

    def tem_recursos(self):
        for no in self.nos:
            if not no.recursos:
                return False
        return True

    def tem_aresta_para_si(self):
        return any(edge[0] == edge[1] for edge in self.grafo.edges)
