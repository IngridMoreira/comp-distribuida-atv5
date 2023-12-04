import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
from flooding_search import FloodingSearch
from informed_flooding_search import InformedFloodingSearch
from random_walk import RandomWalk
from gerenciador_rede import GerenciadorRede
from resultado_busca import ResultadoBusca


class SeletorAlgoritmo:
    def __init__(self, algoritmos):
        self.algoritmos = algoritmos
        self.algoritmo_selecionado = algoritmos[0]

    def definir_algoritmo(self, rotulo):
        self.algoritmo_selecionado = rotulo

    def obter_algoritmo_selecionado(self):
        return self.algoritmo_selecionado


# Função para atualizar o grafo com base na entrada do usuário
def atualizar_grafo(event):
    id_no = caixa_texto_no.text
    id_recurso = caixa_texto_recurso.text
    ttl = int(caixa_texto_ttl.text)

    algoritmo_selecionado = seletor_algoritmo.obter_algoritmo_selecionado()

    resultado_busca = None

    if algoritmo_selecionado == "Busca por Inundação":
        resultado_busca = busca_inundacao.buscar_recurso(id_no, id_recurso, ttl)
    elif algoritmo_selecionado == "Passeio Aleatório":
        resultado_busca = caminhante_aleatorio.buscar_recurso(id_no, id_recurso, ttl)

    exibir_resultado(resultado_busca)


def exibir_resultado(resultado_busca: ResultadoBusca):
    if resultado_busca is not None:
        resultado_texto = ""
        if resultado_busca.rec_encontrado:
            resultado_texto += (
                f"O recurso foi encontrado no nó {resultado_busca.no_rec_encontrado}\n"
            )
            resultado_texto += f"Quantidade de mensagens até encontrar: {resultado_busca.qtd_mens_achar}\n"
        else:
            resultado_texto += "O recurso não foi encontrado\n"
        resultado_texto += (
            f"Quantidade de mensagens totais: {resultado_busca.qtd_mens_totais}"
        )

        texto_resultado.set_text(resultado_texto)
        plt.draw()


def on_hover(event):
    global no_encontrado
    if event.inaxes is not None:
        x, y = event.xdata, event.ydata
        for node, (nx, ny) in posicao.items():
            tolerance = 0.05
            if (
                nx - tolerance < x < nx + tolerance
                and ny - tolerance < y < ny + tolerance
            ):
                if not no_encontrado or no_encontrado.id != node:
                    no_encontrado = next((no for no in rede.nos if no.id == node), None)
                    texto_recursos.set_text(
                        "Recursos: " + ", ".join(map(str, no_encontrado.recursos))
                    )
                    plt.draw()
                break
            else:
                if no_encontrado:
                    no_encontrado = None
                    texto_recursos.set_text("")
                    plt.draw()
                    break


# Crie uma instância do gerenciador de rede
caminho_arquivo = "config.yaml"
gerenciador_rede = GerenciadorRede(caminho_arquivo)

try:
    gerenciador_rede.criar_rede()
    rede = gerenciador_rede.obter_rede()
except ValueError as e:
    print(f"Erro: {e}")
    exit()


# Crie instâncias dos algoritmos de busca
busca_inundacao = FloodingSearch(rede)
busca_informada = InformedFloodingSearch(rede)
caminhante_aleatorio = RandomWalk(rede)


figura, eixo = plt.subplots(figsize=(11, 6))
figura.canvas.mpl_connect("motion_notify_event", on_hover)

posicao = nx.spring_layout(rede.grafo)
nx.draw(rede.grafo, pos=posicao, with_labels=True, font_weight="bold", ax=eixo)


caixa_texto_no = TextBox(plt.axes([0.1, 0.01, 0.1, 0.05]), "Nó")
caixa_texto_recurso = TextBox(plt.axes([0.25, 0.01, 0.1, 0.05]), "Recurso")
caixa_texto_ttl = TextBox(plt.axes([0.4, 0.01, 0.1, 0.05]), "TTL")

# Texto para exibir o resultado
texto_resultado = plt.text(0.05, 0.9, "", transform=figura.transFigure, fontsize=12)
texto_recursos = plt.text(0.7, 0.9, "", transform=figura.transFigure, fontsize=12)


# Crie botões de rádio para a seleção do algoritmo
seletor_algoritmo = SeletorAlgoritmo(["Busca por Inundação", "Passeio Aleatório"])
botoes_radio_algoritmo = RadioButtons(
    plt.axes([0.55, 0.01, 0.3, 0.1]), seletor_algoritmo.algoritmos
)
botoes_radio_algoritmo.on_clicked(seletor_algoritmo.definir_algoritmo)

# Crie um botão para acionar a busca
botao_busca = Button(plt.axes([0.9, 0.01, 0.05, 0.05]), "Buscar")
botao_busca.on_clicked(atualizar_grafo)

no_encontrado = None

plt.show()
