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
        resultado.path = [{"qtd": 0, "list": []} for _ in range(ttl_inicial + 1)]
        nos_visitados = []
        grafo = self.rede.grafo
        while fila:
            origem, atual, ttl = fila.popleft()
            resultado.path[ttl_inicial - ttl]["list"].append(
                {"no": atual, "origem": origem}
            )
            if origem:
                resultado.path[ttl_inicial - ttl]["qtd"] += 1
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
