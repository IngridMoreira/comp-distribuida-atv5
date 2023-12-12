from ...models.resultado_busca import ResultadoBusca
from .search import Search
import random


class RandomWalk(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        resultado = ResultadoBusca()
        resultado.path = []
        if self.rede.grafo.has_node(id_no):
            return self._enviar_pedido_busca(None, id_no, id_recurso, ttl, resultado)

    def _enviar_pedido_busca(self, origem, destino, id_recurso, ttl, resultado):
        resultado = self.add_resultado(destino, origem, resultado)
        if id_recurso in self.rede.grafo.nodes[destino]["recursos"]:
            resultado.no_rec_encontrado = destino
            resultado.rec_encontrado = True
            return resultado
        else:
            if ttl > 0:
                resultado.qtd_mens_totais += 1
                novo_no = self.escolher_no(origem, destino)
                origem = destino
                destino = novo_no
                return self._enviar_pedido_busca(
                    origem, destino, id_recurso, ttl - 1, resultado
                )
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
        return resultado

    def escolher_no(self, origem, destino):
        vizinhos = list(self.rede.grafo.neighbors(destino))
        if origem:
            vizinhos.remove(origem)
        return random.choice(vizinhos)

    def todos_contidos(self, vizinhos, path):
        return set(vizinhos).issubset(path)
