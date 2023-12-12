from collections import deque
import sys

from ...models.resultado_busca import ResultadoBusca

from .search import Search


class FloodingSearch(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        if self.rede.grafo.has_node(id_no):
            return self._enviar_pedido_busca(id_no, id_recurso, ttl)

    def _enviar_pedido_busca(self, origem, id_recurso, ttl):
        fila = deque([(None, origem, ttl)])
        resultado = ResultadoBusca()
        ttl_inicial = ttl
        resultado.path = []
        nos_visitados = []
        grafo = self.rede.grafo
        while fila:
            origem, atual, ttl = fila.popleft()
            resultado = self.add_resultado(atual, origem, resultado, ttl_inicial - ttl)
            if not atual in nos_visitados:
                nos_visitados.append(atual)
                if id_recurso in grafo.nodes[atual]["recursos"]:
                    resultado.no_rec_encontrado = atual
                else:
                    if ttl > 0:
                        for vizinho in grafo.neighbors(atual):
                            if not origem or vizinho != origem:
                                fila.append((atual, vizinho, ttl - 1))
        return resultado

    def add_resultado(self, no_atual, origem, resultado, nivel):
        if nivel > len(resultado.path) - 1:
            resultado.path.append({"list": [], "qtd": 0})
        resultado.path[nivel]["list"].append({"no": no_atual, "origem": origem})
        if origem:
            resultado.path[nivel]["qtd"] += 1
        resultado.qtd_mens_totais += 1
        print(f"{origem} -> {no_atual}")
        return resultado
