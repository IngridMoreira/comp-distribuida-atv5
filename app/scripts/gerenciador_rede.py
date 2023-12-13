from ..models.rede_p2p import RedeP2P


class GerenciadorRede:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.rede = None

    def criar_rede(self, dados_configuracao):
        rede = RedeP2P()

        # Adiciona nós à rede com base nas configurações
        for id_no in range(1, dados_configuracao["num_nodes"] + 1):
            recursos = dados_configuracao["resources"].get(f"n{id_no}", [])
            rede.adicionar_no(f"n{id_no}", recursos)

        # Adiciona arestas à rede com base nas configurações de conexões
        for par_aresta in dados_configuracao["edges"]:
            try:
                aresta = par_aresta.split(",")
                no1 = next(no for no in rede.grafo if no == aresta[0].strip())
                no2 = next(no for no in rede.grafo if no == aresta[1].strip())
            except StopIteration:
                print(f"Erro: Nó com ID {aresta[0]} ou {aresta[1]} não encontrado.")
                continue
            rede.adicionar_aresta(no1, no2)

        # Verifica se as condições necessárias da rede são atendidas
        if self.checar_condicoes(
            rede,
            dados_configuracao["min_neighbors"],
            dados_configuracao["max_neighbors"],
        ):
            self.rede = rede
        else:
            raise ValueError("A rede não atende às condições necessárias")

    def checar_condicoes(self, rede, min_nos, max_nos):
        # Verifica se as condições necessárias da rede são atendidas
        return (
            not rede.esta_particionada()
            and rede.atende_limites(min_nos, max_nos)
            and rede.tem_recursos()
            and not rede.tem_aresta_para_si()
        )

    def obter_rede(self):
        return self.rede
