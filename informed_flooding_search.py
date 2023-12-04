from collections import deque
from search import Search


class InformedFloodingSearch(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        no_origem = next(no for no in self.rede.nos if no.id == id_no)
        achou = self.enviar_pedido_busca(None, no_origem, id_recurso, ttl)
        if not achou:
            print(f"A busca por {id_recurso} não encontrou o recurso.")
        else:
            print(
                f"Informed Flooding: Número de mensagens trocadas até encontrar: {self.contador_mensagens}"
            )
        print(
            f"Informed Flooding: Número total de mensagens trocadas: {self.contador_mensagens_totais}"
        )

    def heuristic(self, node, destination):
        return abs(node.position - destination.position)

    def enviar_pedido_busca(self, origem, destino, id_recurso, ttl):
        fila = deque([(origem, destino, ttl)])
        origem_encontrado = None

        while fila:
            origem, atual, ttl = fila.popleft()

            if origem:
                self.contador_mensagens_totais += 1

                if not origem_encontrado or origem_encontrado == origem:
                    self.contador_mensagens += 1

            if not atual.requisicao_ja_recebida(id_recurso):
                atual.adiciona_requisicao_recebida(id_recurso)

                if atual.tem_recurso(id_recurso):
                    self.anunciar_recurso_encontrado(atual, id_recurso)

                    if origem:
                        origem_encontrado = origem
                    else:
                        origem_encontrado = 0
                else:
                    if ttl > 0:
                        neighbors_sorted = sorted(
                            atual.vizinhos,
                            key=lambda vizinho: self.heuristic(vizinho, destino),
                        )

                        for vizinho in neighbors_sorted:
                            if not origem or vizinho.id != origem.id:
                                fila.append((atual, vizinho, ttl - 1))

        return origem_encontrado is not None
