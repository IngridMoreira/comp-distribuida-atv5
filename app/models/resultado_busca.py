import json


class ResultadoBusca:
    def __init__(self):
        self._rec_encontrado = False
        self._qtd_mens_totais = 0
        self._no_rec_encontrado = None
        self._no_rec = None
        self._id_recurso = None
        self._path = []

    @property
    def rec_encontrado(self):
        return self._rec_encontrado

    @rec_encontrado.setter
    def rec_encontrado(self, value):
        self._rec_encontrado = value

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
    def id_recurso(self):
        return self._id_recurso

    @id_recurso.setter
    def id_recurso(self, value):
        self._id_recurso = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def no_rec(self):
        return self._no_rec

    @no_rec.setter
    def no_rec(self, value):
        self._no_rec = value

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
