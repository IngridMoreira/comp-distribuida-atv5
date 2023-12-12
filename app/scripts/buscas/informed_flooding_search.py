from collections import deque
from ...models.resultado_busca import ResultadoBusca
from .search import Search


class InformedFloodingSearch(Search):
    def __init__(self, rede):
        super().__init__(rede)
        self.cache = {element: None for element in list(rede.grafo.nodes)}

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
            print(self.cache[origem])
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
                if self.cache[origem] and self.cache[origem][id_recurso]:
                    resultado.no_rec_encontrado = self.cache[origem][id_recurso]
                else:
                    if ttl > 0:
                        for vizinho in grafo.neighbors(atual):
                            if not origem or vizinho != origem:
                                fila.append((atual, vizinho, ttl - 1))
        if resultado.no_rec_encontrado:
            if not self.cache[origem]:
                self.cache[origem] = {}
            if self.cache[origem][id_recurso]:
                self.cache[origem][id_recurso].append(resultado.no_rec_encontrado)
            else:
                self.cache[origem][id_recurso] = [resultado.no_rec_encontrado]

        return resultado
