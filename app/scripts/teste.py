from ast import List

from ..scripts.buscas.search import Search
from ..models.rede_p2p import RedeP2P
from ..models.resultado_busca import ResultadoBusca
from ..scripts.buscas.informed_flooding_search import InformedFloodingSearch
from ..scripts.buscas.informed_random_walk import InformedRandomWalk
from ..scripts.buscas.random_walk import RandomWalk
from ..scripts.buscas.flooding_search import FloodingSearch
import numpy as np


def criar_teste(rede: RedeP2P):
    flooding_search = FloodingSearch(rede)
    random_walk = RandomWalk(rede)
    informed_flooding_search = InformedFloodingSearch(rede)
    informed_random_walk = InformedRandomWalk(rede)
    algoritmos: List[Search] = [
        flooding_search,
        random_walk,
        informed_flooding_search,
        informed_random_walk,
    ]

    # no, recurso e ttl
    testes = [
        [
            ("n1", "r12", 10),
            ("n4", "r5", 10),
            ("n8", "r9", 10),
            ("n12", "r6", 10),
            ("n3", "r5", 10),
            ("n6", "r4", 10),
            ("n10", "r2", 10),
            ("n2", "r8", 10),
        ],
        [
            ("n1", "r12", 10),
            ("n4", "r5", 10),
            ("n8", "r9", 10),
            ("n12", "r6", 10),
            ("n3", "r5", 10),
            ("n6", "r4", 10),
            ("n10", "r2", 10),
            ("n2", "r8", 10),
        ],
    ]

    resultado_teste = []
    for i, teste in enumerate(testes):
        resultado_teste.append({"teste": teste, "resultados": {}})
        for alg in algoritmos:
            rede.limpar_cache()
            aux = {"qtd_mens": [], "qtd_nos": []}
            for no, recurso, ttl in teste:
                res_busca = alg.buscar_recurso(no, recurso, ttl)
                aux["qtd_mens"].append(res_busca.qtd_mens_totais)
                aux["qtd_nos"].append(len(res_busca.path[-1]["nos_visitados"]))
            resultado_teste[i]["resultados"][alg.__class__.__name__] = {
                "qtd_mens": {
                    "media": np.mean(aux["qtd_mens"]),
                    "mediana": np.median(aux["qtd_mens"]),
                },
                "qtd_nos": {
                    "media": np.mean(aux["qtd_nos"]),
                    "mediana": np.median(aux["qtd_nos"]),
                },
            }
    return resultado_teste
