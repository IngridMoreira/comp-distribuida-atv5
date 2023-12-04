import copy
from resultado_busca import ResultadoBusca


class Search:
    def __init__(self, rede):
        self.rede = rede
        self.contador_mensagens = 0
        self.resultado = ResultadoBusca()

    def anunciar_recurso_encontrado(self, id_no, id_recurso):
        self.resultado.rec_encontrado = True
        self.resultado.no_rec_encontrado = id_no
        self.resultado._id_recurso = id_recurso

    def buscar_recurso(self, id_no, id_recurso, ttl):
        raise NotImplementedError(
            "Método buscar_recurso deve ser implementado nas subclasses"
        )

    def limpar_resultado(self):
        aux = copy.deepcopy(self.resultado)
        self.resultado.rec_encontrado = False
        self.resultado.qtd_mens_achar = 0
        self.resultado.qtd_mens_totais = 0
        self.resultado.no_rec_encontrado = None
        self.resultado.qtd_nos_envolvidos = 0
        self.resultado.id_recurso = None
        self.contador_mensagens = 0
        self.rede.limpar_requisicoes_recebidas()
        return aux
