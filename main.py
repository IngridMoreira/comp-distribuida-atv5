import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
from flooding_search import FloodingSearch
from informed_flooding_search import InformedFloodingSearch
from random_walk import RandomWalk
from gerenciador_rede import GerenciadorRede


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

    if algoritmo_selecionado == "Busca por Inundação":
        busca_inundacao.buscar_recurso(id_no, id_recurso, ttl)
    elif algoritmo_selecionado == "Busca Informada por Inundação":
        busca_informada.buscar_recurso(id_no, id_recurso, ttl)
    elif algoritmo_selecionado == "Caminhada Aleatória":
        caminhante_aleatorio.buscar_recurso(id_no, id_recurso, ttl)


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

# Crie a figura principal e o eixo com dimensões maiores
figura, eixo = plt.subplots(figsize=(11, 6))

posicao = nx.spring_layout(rede.grafo)
nx.draw(rede.grafo, pos=posicao, with_labels=True, font_weight="bold", ax=eixo)

# Crie caixas de texto para a entrada do usuário
caixa_texto_no = TextBox(plt.axes([0.1, 0.01, 0.1, 0.05]), "Nó")
caixa_texto_recurso = TextBox(plt.axes([0.25, 0.01, 0.1, 0.05]), "Recurso")
caixa_texto_ttl = TextBox(plt.axes([0.4, 0.01, 0.1, 0.05]), "TTL")

# Crie botões de rádio para a seleção do algoritmo
seletor_algoritmo = SeletorAlgoritmo(
    ["Busca por Inundação", "Busca Informada por Inundação", "Caminhada Aleatória"]
)
botoes_radio_algoritmo = RadioButtons(
    plt.axes([0.55, 0.01, 0.3, 0.1]), seletor_algoritmo.algoritmos
)
botoes_radio_algoritmo.on_clicked(seletor_algoritmo.definir_algoritmo)

# Crie um botão para acionar a busca
botao_busca = Button(plt.axes([0.9, 0.01, 0.05, 0.05]), "Buscar")
botao_busca.on_clicked(atualizar_grafo)

# Exiba o gráfico
plt.show()
