import sys
from flask import Flask, session
import yaml

from app.routes import add_routes
from .scripts.gerenciador_rede import GerenciadorRede

app = Flask(__name__)


def ler_config():
    with open("data/config.yaml", "r") as arquivo:
        config = yaml.safe_load(arquivo)
    return config


def criar_rede(dados_configuracao):
    gerenciador = GerenciadorRede("data/config.yaml")
    gerenciador.criar_rede(dados_configuracao)
    return gerenciador.obter_rede()


def create_app():
    dados_configuracao = ler_config()
    rede = criar_rede(dados_configuracao)
    app.config["REDE"] = rede
    app.secret_key = "12345"
    add_routes(app)
    return app
