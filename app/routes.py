# routes.py
import json
from flask import render_template, request, session

from .scripts.buscas.informed_flooding_search import InformedFloodingSearch
from app.scripts.buscas.informed_random_walk import InformedRandomWalk

from .scripts.buscas.random_walk import RandomWalk
from .scripts.buscas.flooding_search import FloodingSearch

import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import sys

frame_atual = 0


def add_routes(app):
    random_walk = RandomWalk(app.config.get("REDE"))
    flooding_search = FloodingSearch(app.config.get("REDE"))
    # informed_random_walk = InformedRandomWalk(app.config.get("REDE"))
    # informed_flooding_search = InformedFloodingSearch(app.config.get("REDE"))

    @app.template_filter("msg_sum")
    @app.template_filter("json_decode")
    def json_decode(value):
        return json.loads(value)

    @app.route("/")
    def home():
        rede = app.config.get("REDE")
        img_data = plotar_grafo(rede.grafo)
        return render_template("index.html", img_data=img_data)

    @app.route("/buscar", methods=["POST"])
    def buscar():
        global frame_atual
        frame_atual = 0
        rede = app.config.get("REDE")
        nos = request.form.get("nos")
        recurso = request.form.get("recurso")
        ttl = int(request.form.get("ttl"))
        algoritmo = request.form.get("algoritmo")
        resultado_busca = selecionar_algoritmo(algoritmo).buscar_recurso(
            nos, recurso, ttl
        )
        resultado_completo = {
            "resultado_busca": resultado_busca.to_json(),
            "algoritmo": algoritmo,
            "id_no": nos,
        }
        session["resultado_busca"] = json.dumps(resultado_completo)
        img_data = animacao(rede, frame_atual)
        return render_template(
            "animacao.html",
            resultado_completo=resultado_completo,
            img_data=img_data,
            frame_atual=frame_atual,
            msg_sum=msg_sum(resultado_busca.path),
        )

    @app.route("/mudar_frame", methods=["POST"])
    def mudar_frame():
        global frame_atual
        rede = app.config.get("REDE")
        acao = request.json.get("acao")
        if acao == "anterior":
            frame_atual -= 1
        elif acao == "proximo":
            frame_atual += 1
        img_data = animacao(rede, frame_atual)

        return render_template(
            "animacao.html",
            resultado_completo=json.loads(session.get("resultado_busca")),
            img_data=img_data,
            frame_atual=frame_atual,
            msg_sum=msg_sum(
                json.loads(
                    json.loads(session.get("resultado_busca"))["resultado_busca"]
                )["_path"]
            ),
        )

    def selecionar_algoritmo(algoritmo):
        if algoritmo == "Busca por Inundação":
            return flooding_search
        if algoritmo == "Passeio Aleatório":
            return random_walk
        if algoritmo == "Busca por Inundação Informada":
            return informed_flooding_search
        if algoritmo == "Passeio Aleatório Informado":
            return informed_random_walk


def plotar_grafo(grafo):
    pos = nx.spring_layout(grafo, seed=1)

    plt.figure(figsize=(8, 8))
    nx.draw(
        grafo,
        pos,
        with_labels=True,
        font_weight="bold",
        node_size=700,
        node_color="skyblue",
    )

    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)
    return base64.b64encode(image_stream.read()).decode("utf-8")


def get_level(resultado_busca, no_com_recurso):
    path = resultado_busca["_path"]
    for index, value in enumerate(path):
        nos_atuais = value["list"]
        ids_nos_atuais = [node_info["no"] for node_info in nos_atuais]
        if no_com_recurso in ids_nos_atuais:
            return index


def set_node_colors(grafo, passo):
    resultado_busca = json.loads(session.get("resultado_busca"))
    resultado_busca["resultado_busca"] = json.loads(resultado_busca["resultado_busca"])
    nos_atuais = resultado_busca["resultado_busca"]["_path"][passo]["list"]
    ids_nos_atuais = [node_info["no"] for node_info in nos_atuais]
    no_com_recurso = resultado_busca["resultado_busca"]["_no_rec_encontrado"]
    nivel_encontrou = get_level(resultado_busca["resultado_busca"], no_com_recurso)
    node_colors = [
        "green"
        if no == no_com_recurso and nivel_encontrou <= passo
        else "red"
        if no in ids_nos_atuais
        else "skyblue"
        for no in grafo
    ]

    return node_colors


def criar_frame(grafo, posicao, passo):
    plt.figure(figsize=(8, 8))
    node_labels = {
        node: f"{node} : {grafo.nodes[node].get('recursos', '')}"
        for node in grafo.nodes
    }
    node_colors = set_node_colors(grafo, passo)
    nx.draw(
        grafo,
        posicao,
        with_labels=True,
        labels=node_labels,
        font_weight="bold",
        node_size=700,
        node_color=node_colors,
    )


def obter_dados_imagem():
    stream_imagem = BytesIO()
    plt.savefig(stream_imagem, format="png")
    stream_imagem.seek(0)
    return base64.b64encode(stream_imagem.read()).decode("utf-8")


def animacao(rede, passo):
    grafo = rede.grafo
    posicao = nx.spring_layout(grafo, seed=1)
    criar_frame(grafo, posicao, passo)
    dados_imagem = obter_dados_imagem()

    return dados_imagem


def msg_sum(path):
    global frame_atuals
    return sum(item.get("qtd", 0) for i, item in enumerate(path) if i <= frame_atual)
