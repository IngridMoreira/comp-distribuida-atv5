import copy

from ...models.rede_p2p import RedeP2P

from ...models.resultado_busca import ResultadoBusca


class Search:
    def __init__(self, rede: RedeP2P):
        self.rede = rede

    def buscar_recurso(self, id_no, id_recurso, ttl) -> ResultadoBusca:
        raise NotImplementedError(
            "Método buscar_recurso deve ser implementado nas subclasses"
        )

    def limpar_resultado(resultado: ResultadoBusca) -> ResultadoBusca:
        aux = copy.deepcopy(resultado)
        resultado.rec_encontrado = False
        resultado.qtd_mens_totais = 0
        resultado.no_rec_encontrado = None
        resultado.id_recurso = None
        resultado.path = []
        return aux
