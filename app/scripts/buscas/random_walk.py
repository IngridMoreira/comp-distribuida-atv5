from ...models.resultado_busca import ResultadoBusca
from .search import Search
import random

path = set()


class RandomWalk(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        resultado = ResultadoBusca()
        resultado.path = []
        path.clear()
        if self.rede.grafo.has_node(id_no):
            return self._enviar_pedido_busca(None, id_no, id_recurso, ttl, resultado)

    def _enviar_pedido_busca(self, origem, destino, id_recurso, ttl, resultado):
        resultado = self.add_resultado(destino, origem, resultado)
        path.add(destino)
        if id_recurso in self.rede.grafo.nodes[destino]["recursos"]:
            resultado.no_rec_encontrado = destino
            resultado.rec_encontrado = True
            return resultado
        else:
            if ttl > 0:
                vizinhos = list(self.rede.grafo.neighbors(destino))
                vizinhos_n_visitados = [
                    vizinho for vizinho in vizinhos if vizinho not in path
                ]
                while vizinhos_n_visitados:
                    vizinhos_n_visitados = [
                        vizinho for vizinho in vizinhos if vizinho not in path
                    ]
                    if vizinhos_n_visitados:
                        proximo_no = random.choice(vizinhos_n_visitados)
                        self._enviar_pedido_busca(
                            destino, proximo_no, id_recurso, ttl - 1, resultado
                        )
                        resultado = self.add_resultado(destino, proximo_no, resultado)
                return resultado
            else:
                return resultado

    def add_resultado(self, no_atual, origem, resultado):
        if not origem:
            resultado.path.append(
                {"list": [{"no": no_atual, "origem": origem}], "qtd": 0}
            )
        else:
            resultado.path.append(
                {"list": [{"no": no_atual, "origem": origem}], "qtd": 1}
            )
        resultado.qtd_mens_totais += 1
        print(f"{origem} -> {no_atual}")
        return resultado
