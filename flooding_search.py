from collections import deque
import copy
from resultado_busca import ResultadoBusca
from search import Search


class FloodingSearch(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        # Encontrar o nó de origem na rede
        no_origem = next((no for no in self.rede.nos if no.id == id_no), None)

        # Iniciar o envio do pedido de busca
        self.enviar_pedido_busca(no_origem, id_recurso, ttl)

        return self.limpar_resultado()

    def enviar_pedido_busca(self, origem, id_recurso, ttl):
        # Inicializar fila de busca usando deque
        fila = deque([(None, origem, ttl)])
        origem_encontrado = None
        print(id_recurso)
        # Loop principal para realizar a busca por inundação
        while fila:
            origem, atual, ttl = fila.popleft()

            print(f"{atual.id} - {ttl}")

            # Contabilizar mensagens totais trocadas
            if origem:
                self.resultado.qtd_mens_totais += 1

                # Contabilizar mensagens trocadas apenas para a busca específica
                if not origem_encontrado or origem_encontrado.id == origem.id:
                    self.contador_mensagens += 1
                else:
                    if self.contador_mensagens > 0:
                        self.resultado.qtd_mens_achar = self.contador_mensagens

            # Verificar se o nó atual já recebeu uma requisição para o recurso
            if not atual.requisicao_ja_recebida(id_recurso):
                atual.adiciona_requisicao_recebida(id_recurso)

                # Verificar se o nó atual possui o recurso desejado
                if atual.tem_recurso(id_recurso):
                    self.anunciar_recurso_encontrado(atual.id, id_recurso)

                    # Atualizar o nó de origem encontrado
                    if origem:
                        origem_encontrado = copy.deepcopy(origem)
                    else:
                        origem_encontrado = 0
                else:
                    # Adicionar vizinhos à fila para continuar a busca
                    if ttl > 0:
                        for vizinho in atual.vizinhos:
                            if not origem or vizinho.id != origem.id:
                                fila.append((atual, vizinho, ttl - 1))
