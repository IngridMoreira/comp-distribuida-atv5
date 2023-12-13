from collections import deque
import sys

from ...models.resultado_busca import ResultadoBusca

from .search import Search


class InformedFloodingSearch(Search):
    def __init__(self, rede):
        super().__init__(rede)
        for node in self.rede.grafo.nodes:
            self.rede.grafo.nodes[node]["cache"] = {}

    def buscar_recurso(self, id_no, id_recurso, ttl):
        self.visitados.clear()
        if self.rede.grafo.has_node(id_no):
            resultado = ResultadoBusca()
            fila = deque([(None, id_no, ttl, [id_no])])

            return self._enviar_pedido_busca(fila, id_recurso, ttl, resultado, ttl)

    def _enviar_pedido_busca(self, fila, id_recurso, ttl, resultado, ttl_inicial):
        grafo = self.rede.grafo
        while fila:
            origem, atual, ttl, path = fila.popleft()
            if not atual in self.visitados:
                self.visitados.append(atual)
                if id_recurso in grafo.nodes[atual]["recursos"]:
                    if not resultado.no_rec_encontrado:
                        resultado.rec_encontrado = True
                        resultado.no_rec_encontrado = atual
                        resultado.no_rec = [atual]
                    self.add_valor_cache(resultado, id_recurso, path)
                elif id_recurso in self.rede.grafo.nodes[atual]["cache"]:
                    resultado.rec_encontrado = True
                    resultado.no_rec_encontrado = atual
                    resultado.no_rec = self.rede.grafo.nodes[atual]["cache"][id_recurso]
                else:
                    if ttl > 0:
                        for vizinho in grafo.neighbors(atual):
                            if not origem or vizinho != origem:
                                fila.append(
                                    (
                                        atual,
                                        vizinho,
                                        ttl - 1,
                                        path + [vizinho],
                                    )
                                )

            self.add_resultado(atual, origem, resultado, ttl_inicial - ttl, ttl)
            resultado = self._enviar_pedido_busca(
                fila, id_recurso, ttl - 1, resultado, ttl_inicial
            )

        return resultado

    def add_valor_cache(self, resultado, id_recurso, path):
        for no in path:
            if resultado.no_rec_encontrado:
                if not id_recurso in self.rede.grafo.nodes[no]["cache"]:
                    self.rede.grafo.nodes[no]["cache"][id_recurso] = [
                        resultado.no_rec_encontrado
                    ]
                else:
                    if (
                        resultado.no_rec_encontrado
                        not in self.rede.grafo.nodes[no]["cache"][id_recurso]
                    ):
                        self.rede.grafo.nodes[no]["cache"][id_recurso].append(
                            resultado.no_rec_encontrado
                        )

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
