from collections import deque
from search import Search


class FloodingSearch(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        # Encontrar o nó de origem na rede
        no_origem = next(no for no in self.rede.nos if no.id == id_no)

        # Iniciar o envio do pedido de busca
        achou = self.enviar_pedido_busca(no_origem, id_recurso, ttl)

        # Exibir mensagem caso o recurso não seja encontrado
        if not achou:
            print(f"A busca por {id_recurso} não encontrou o recurso.")
        else:
            print(
                f"Flooding: Número de mensagens trocadas até encontrar: {self.contador_mensagens}"
            )
        print(
            f"Flooding: Número total de mensagens trocadas: {self.contador_mensagens_totais}"
        )

    def enviar_pedido_busca(self, origem, id_recurso, ttl):
        # Inicializar fila de busca usando deque
        fila = deque([(None, origem, ttl)])
        origem_encontrado = None

        # Loop principal para realizar a busca por inundação
        while fila:
            origem, atual, ttl = fila.popleft()

            # Contabilizar mensagens totais trocadas
            if origem:
                self.contador_mensagens_totais += 1

                # Contabilizar mensagens trocadas apenas para a busca específica
                if not origem_encontrado or origem_encontrado == origem:
                    self.contador_mensagens += 1

            # Verificar se o nó atual já recebeu uma requisição para o recurso
            if not atual.requisicao_ja_recebida(id_recurso):
                atual.adiciona_requisicao_recebida(id_recurso)

                # Verificar se o nó atual possui o recurso desejado
                if atual.tem_recurso(id_recurso):
                    self.anunciar_recurso_encontrado(atual, id_recurso)

                    # Atualizar o nó de origem encontrado
                    if origem:
                        origem_encontrado = origem
                    else:
                        origem_encontrado = 0
                else:
                    # Adicionar vizinhos à fila para continuar a busca
                    if ttl > 0:
                        for vizinho in atual.vizinhos:
                            if not origem or vizinho.id != origem.id:
                                fila.append((atual, vizinho, ttl - 1))

        # Retornar True se o recurso foi encontrado, False caso contrário
        return origem_encontrado is not None
