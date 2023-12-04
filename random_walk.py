from search import Search
import random


class RandomWalk(Search):
    def buscar_recurso(self, id_no, id_recurso, ttl):
        # Encontrar o nó de origem na rede
        no_origem = next(no for no in self.rede.nos if no.id == id_no)
        achou = self.enviar_pedido_busca(no_origem, id_recurso, ttl)
        if not achou:
            print(f"A busca por {id_recurso} não encontrou o recurso.")
        print(
            f"Passeio Aleatório: Número total de mensagens trocadas: {self.contador_mensagens_totais}"
        )

    # Se o único nó vizinho é o anterior, ele volta e tenta outro caminho?
    def enviar_pedido_busca(self, origem, id_recurso, ttl):
        no_atual = origem
        while True:
            if no_atual.tem_recurso(id_recurso):
                self.anunciar_recurso_encontrado(no_atual, id_recurso)
                return True
            else:
                if ttl > 0:
                    self.contador_mensagens_totais += 1
                    no_atual = random.choice(no_atual.vizinhos)
                    ttl -= 1
                else:
                    return False
