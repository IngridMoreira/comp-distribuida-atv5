class ResultadoBusca:
    def __init__(self):
        self._rec_encontrado = False
        self._qtd_mens_achar = 0
        self._qtd_mens_totais = 0
        self._no_rec_encontrado = None
        self._qtd_nos_envolvidos = 0
        self._id_recurso = None

    @property
    def rec_encontrado(self):
        return self._rec_encontrado

    @rec_encontrado.setter
    def rec_encontrado(self, value):
        self._rec_encontrado = value

    @property
    def qtd_mens_achar(self):
        return self._qtd_mens_achar

    @qtd_mens_achar.setter
    def qtd_mens_achar(self, value):
        self._qtd_mens_achar = value

    @property
    def qtd_mens_totais(self):
        return self._qtd_mens_totais

    @qtd_mens_totais.setter
    def qtd_mens_totais(self, value):
        self._qtd_mens_totais = value

    @property
    def no_rec_encontrado(self):
        return self._no_rec_encontrado

    @no_rec_encontrado.setter
    def no_rec_encontrado(self, value):
        self._no_rec_encontrado = value

    @property
    def qtd_nos_envolvidos(self):
        return self._qtd_nos_envolvidos

    @qtd_nos_envolvidos.setter
    def qtd_nos_envolvidos(self, value):
        self._qtd_nos_envolvidos = value

    @property
    def id_recurso(self):
        return self._id_recurso

    @id_recurso.setter
    def id_recurso(self, value):
        self._id_recurso = value
