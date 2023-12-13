from collections import deque
import sys

from ...models.resultado_busca import ResultadoBusca

from .search import Search


class FloodingSearch(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        self.visitados.clear()
        if self.rede.grafo.has_node(id_no):
            return self._enviar_pedido_busca(id_no, id_recurso, ttl)

    def _enviar_pedido_busca(self, origem, id_recurso, ttl):
        fila = deque([(None, origem, ttl)])
        resultado = ResultadoBusca()
        ttl_inicial = ttl
        resultado.path = []
        grafo = self.rede.grafo
        while fila:
            origem, atual, ttl = fila.popleft()
            if not atual in self.visitados:
                self.visitados.append(atual)
                if id_recurso in grafo.nodes[atual]["recursos"]:
                    resultado.rec_encontrado = True
                    resultado.no_rec_encontrado = atual
                    resultado.no_rec = [atual]
                else:
                    if ttl > 0:
                        for vizinho in grafo.neighbors(atual):
                            if not origem or vizinho != origem:
                                fila.append((atual, vizinho, ttl - 1))
            resultado = self.add_resultado(
                atual, origem, resultado, ttl_inicial - ttl, ttl
            )
        return resultado

    def add_resultado(self, no_atual, origem, resultado, nivel, ttl):
        if nivel > len(resultado.path) - 1:
            resultado.path.append({"list": [], "qtd": 0})
        resultado.path[nivel]["list"].append(
            {
                "no": no_atual,
                "origem": origem,
            }
        )
        if origem:
            resultado.path[nivel]["qtd"] += 1
            resultado.qtd_mens_totais += 1
        resultado.path[nivel]["ttl"] = ttl
        resultado.path[nivel]["nos_visitados"] = self.visitados.copy()

        return resultado
