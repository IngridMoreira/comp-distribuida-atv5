import yaml
import networkx as nx
import matplotlib.pyplot as plt
from rede_p2p import RedeP2P
from rede_p2p import No


contador_mensagens = 0


def ler_configuracao(caminho_arquivo):
    with open(caminho_arquivo, "r") as arquivo:
        dados = yaml.safe_load(arquivo)
    return dados


def visualizar_rede(rede):
    posicao = nx.spring_layout(rede.grafo)
    nx.draw(rede.grafo, posicao, with_labels=True, font_weight="bold")
    plt.show()


def checar_condicoes(rede, min_nos, max_nos):
    return (
        not rede.esta_particionada()
        and rede.atende_limites(min_nos, max_nos)
        and rede.tem_recursos()
        and not rede.tem_aresta_para_si()
    )


def criar_rede():
    arquivo_configuracao = "config.yaml"
    dados_configuracao = ler_configuracao(arquivo_configuracao)

    rede = RedeP2P()

    for id_no in range(1, dados_configuracao["num_nodes"] + 1):
        recursos = dados_configuracao["resources"].get(f"n{id_no}", [])
        no = No(f"n{id_no}", recursos)
        rede.adicionar_no(no)

    for par_aresta in dados_configuracao["edges"]:
        try:
            aresta = par_aresta.split(",")
            no1 = next(no for no in rede.nos if no.id == aresta[0].strip())
            no2 = next(no for no in rede.nos if no.id == aresta[1].strip())
        except StopIteration:
            print(f"Erro: No com ID {aresta[0]} ou {aresta[1]} não encontrado.")
            continue
        rede.adicionar_aresta(no1, no2)

    if checar_condicoes(
        rede, dados_configuracao["min_neighbors"], dados_configuracao["max_neighbors"]
    ):
        return rede
    else:
        raise ValueError("A rede não atende às condições necessárias")


def anunciar_recurso_encontrado(no, recurso_alvo):
    print(f"Recurso {recurso_alvo} encontrado pelo nó {no.id}")


def flooding_busca_recurso(rede, id_no, id_recurso, ttl):
    no_origem = next(no for no in rede.nos if no.id == id_no)
    achou = False
    for vizinho in no_origem.vizinhos:
        resultado = enviar_pedido_busca(no_origem, vizinho, id_recurso, ttl - 1)
        if resultado:
            achou = True
    if not achou:
        print(f"A busca por {id_recurso} não encontrou o recurso.")


def enviar_pedido_busca(origem, destino, id_recurso, ttl):
    global contador_mensagens
    contador_mensagens += 1
    achou = False
    print(
        f"Enviando busca para o nó {destino.id} pelo nó {origem.id} buscando recurso {id_recurso} com TTL {ttl}"
    )
    if destino.tem_recurso(id_recurso) and not destino.requisicao_ja_recebida(
        id_recurso
    ):
        anunciar_recurso_encontrado(destino, id_recurso)
        achou = True
    else:
        if ttl > 0:
            for vizinho in destino.vizinhos:
                if (
                    not vizinho.requisicao_ja_recebida(id_recurso)
                    and not vizinho.id == origem.id
                ):
                    resultado = enviar_pedido_busca(
                        destino, vizinho, id_recurso, ttl - 1
                    )
                    if resultado and not achou:
                        achou = resultado
    destino.adiciona_requisicao_recebida(id_recurso)
    return achou


if __name__ == "__main__":
    rede = criar_rede()
    # visualizar_rede(rede)

    # flooding = 'f'
    # informed_flooding = 'if'
    # random_walk = 'rw'
    # infomed_random_walk = 'irw'

    id_no = "n1"
    id_recurso = "r100"
    ttl = 10
    algo = "f"

    contador_mensagens = 0

    flooding_busca_recurso(rede, id_no, id_recurso, ttl)
    print(f"Flooding: Número total de mensagens trocadas: {contador_mensagens}")

    # visualizar_rede(rede)
