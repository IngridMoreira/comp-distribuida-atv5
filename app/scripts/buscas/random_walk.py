from ...models.resultado_busca import ResultadoBusca
from .search import Search
import random


class RandomWalk(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        self.visitados.clear()
        resultado = ResultadoBusca()
        resultado.path = []
        if self.rede.grafo.has_node(id_no):
            # return self._enviar_pedido_busca(None, id_no, id_recurso, ttl, resultado)
            return self._enviar_pedido_busca(
                None, id_no, id_recurso, ttl, resultado, id_no
            )  # Com nó inicial (Algoritmo 2)

    # Não deixa uma mensagem ser enviada caso o nó já tenha sido visitado, pois parte do pressuposto que o nó tem acesso ao caminha percorrido pela busca.
    # Não chega a mesma profundidade que a busca por inundação
    # def _enviar_pedido_busca(self, origem, destino, id_recurso, ttl, resultado):
    #     if destino not in self.visitados:
    #         self.visitados.append(destino)
    #     resultado = self.add_resultado(destino, origem, resultado, ttl)
    #     if id_recurso in self.rede.grafo.nodes[destino]["recursos"]:
    #         resultado.no_rec_encontrado = destino
    #         resultado.rec_encontrado = True
    #         return resultado
    #     else:
    #         if ttl > 0:
    #             vizinhos = list(self.rede.grafo.neighbors(destino))
    #             vizinhos_n_visitados = [
    #                 vizinho for vizinho in vizinhos if vizinho not in self.visitados
    #             ]
    #             while vizinhos_n_visitados:
    #                 vizinhos_n_visitados = [
    #                     vizinho for vizinho in vizinhos if vizinho not in self.visitados
    #                 ]
    #                 if vizinhos_n_visitados:
    #                     proximo_no = random.choice(vizinhos_n_visitados)
    #                     self._enviar_pedido_busca(
    #                         destino, proximo_no, id_recurso, ttl - 1, resultado
    #                     )
    #                     resultado = self.add_resultado(destino, proximo_no, resultado, ttl)
    #             return resultado
    #         else:
    #             return resultado

    # A mensagem é enviada normalmente independente se o nó já foi ou não visitado. Tem a mesma profundidade que a inundação
    # def _enviar_pedido_busca(
    #     self, origem, destino, id_recurso, ttl, resultado, no_inicial
    # ):
    #     if destino not in self.visitados:
    #         self.visitados.append(destino)
    #     resultado = self.add_resultado(destino, origem, resultado, ttl)
    #     if id_recurso in self.rede.grafo.nodes[destino]["recursos"]:
    #         resultado.no_rec_encontrado = destino
    #         resultado.rec_encontrado = True
    #         return resultado
    #     else:
    #         if ttl > 0:
    #             vizinhos_escolhidos = [no_inicial, origem]
    #             vizinhos = list(self.rede.grafo.neighbors(destino))
    #             vizinhos_n_visitados = vizinhos
    #             while vizinhos_n_visitados:
    #                 vizinhos_n_visitados = [
    #                     vizinho
    #                     for vizinho in vizinhos
    #                     if vizinho not in vizinhos_escolhidos
    #                 ]
    #                 if vizinhos_n_visitados:
    #                     proximo_no = random.choice(vizinhos_n_visitados)
    #                     vizinhos_escolhidos.append(proximo_no)
    #                     self._enviar_pedido_busca(
    #                         destino,
    #                         proximo_no,
    #                         id_recurso,
    #                         ttl - 1,
    #                         resultado,
    #                         no_inicial,
    #                     )
    #                     resultado = self.add_resultado(
    #                         destino, proximo_no, resultado, ttl
    #                     )
    #             return resultado
    #         else:
    #             return resultado

    # Mensagem chega até o nó que já recebeu, mas não é repassada
    def _enviar_pedido_busca(
        self, origem, destino, id_recurso, ttl, resultado, no_inicial
    ):
        if destino not in self.visitados:
            self.visitados.append(destino)
        resultado = self.add_resultado(destino, origem, resultado, ttl)
        if id_recurso in self.rede.grafo.nodes[destino]["recursos"]:
            resultado.no_rec_encontrado = destino
            resultado.no_rec = [destino]
            resultado.rec_encontrado = True
            return resultado
        else:
            if ttl > 0:
                vizinhos_escolhidos = [no_inicial, destino]
                vizinhos = list(self.rede.grafo.neighbors(destino))
                vizinhos_n_visitados = vizinhos
                while vizinhos_n_visitados:
                    vizinhos_n_visitados = [
                        vizinho
                        for vizinho in vizinhos
                        if vizinho not in vizinhos_escolhidos
                    ]
                    if vizinhos_n_visitados:
                        proximo_no = random.choice(vizinhos_n_visitados)
                        vizinhos_escolhidos.append(proximo_no)
                        if proximo_no not in self.visitados:
                            self._enviar_pedido_busca(
                                destino,
                                proximo_no,
                                id_recurso,
                                ttl - 1,
                                resultado,
                                no_inicial,
                            )
                            resultado = self.add_resultado(
                                destino, proximo_no, resultado, ttl
                            )
                return resultado
            else:
                return resultado

    def add_resultado(self, no_atual, origem, resultado, ttl):
        if not origem:
            resultado.path.append(
                {
                    "list": [{"no": no_atual, "origem": origem}],
                    "qtd": 0,
                    "ttl": ttl,
                    "nos_visitados": self.visitados.copy(),
                }
            )
        else:
            resultado.path.append(
                {
                    "list": [{"no": no_atual, "origem": origem}],
                    "qtd": 1,
                    "ttl": ttl,
                    "nos_visitados": self.visitados.copy(),
                }
            )
        resultado.qtd_mens_totais += 1
        return resultado
