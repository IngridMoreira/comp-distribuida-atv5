from ...models.resultado_busca import ResultadoBusca
from .search import Search
import random


class InformedRandomWalk(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        if self.rede.grafo.has_node(id_no):
            return self._enviar_pedido_busca(id_no, id_recurso, ttl)

    def enviar_pedido_busca(self, origem, id_recurso, ttl):
        resultado = ResultadoBusca()
        ttl_inicial = ttl
        grafo = self.rede.grafo
        no_anterior = None
        no_atual = origem
        while True:
            print(f"{no_anterior} -> {no_atual} - ttl{ttl}")
            if id_recurso in grafo.nodes[no_atual]["recursos"]:
                resultado.no_rec_encontrado = no_atual
                return resultado
            else:
                if ttl > 0:
                    resultado.qtd_mens_totais += 1
                    no_anterior = no_atual
                    while no_anterior == no_atual:
                        no_atual = random.choice(grafo.neighbors(no_atual))
                    ttl -= 1
                else:
                    break
