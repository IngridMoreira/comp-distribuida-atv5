class Search:
    def __init__(self, rede):
        self.rede = rede
        self.contador_mensagens = 0
        self.contador_mensagens_totais = 0

    def anunciar_recurso_encontrado(self, no, recurso_alvo):
        print(f"Recurso {recurso_alvo} encontrado pelo nó {no.id}")

    def buscar_recurso(self, id_no, id_recurso, ttl):
        raise NotImplementedError(
            "Método buscar_recurso deve ser implementado nas subclasses"
        )
