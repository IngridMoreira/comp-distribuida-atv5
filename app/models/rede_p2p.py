import networkx as nx


class RedeP2P:
    def __init__(self):
        self.grafo = nx.Graph()

    def adicionar_no(self, no, recursos):
        self.grafo.add_node(no, recursos=recursos)

    def adicionar_aresta(self, no1, no2):
        self.grafo.add_edge(no1, no2)

    def esta_particionada(self):
        return not nx.is_connected(self.grafo)

    def atende_limites(self, min_vizinhos, max_vizinhos):
        for no in self.grafo.nodes:
            num_vizinhos = len(list(self.grafo.neighbors(no)))
            if num_vizinhos < min_vizinhos or num_vizinhos > max_vizinhos:
                return False
        return True

    def tem_recursos(self):
        for no in self.grafo.nodes:
            if not self.grafo.nodes[no]["recursos"]:
                return False
        return True

    def tem_aresta_para_si(self):
        return any(edge[0] == edge[1] for edge in self.grafo.edges())

    def limpar_cache(self):
        for node in self.grafo.nodes:
            self.grafo.nodes[node]["cache"] = {}
