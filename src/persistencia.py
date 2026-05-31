import json
import os

FICHEIROS = {
    "clubes": "clubes.json",
    "jogadores": "jogadores.json",
    "treinadores": "treinadores.json",
    "jogos": "jogos.json"
}

def guardar(ficheiro: str, dados: dict):
    with open(ficheiro, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar(ficheiro: str) -> dict:
    if os.path.exists(ficheiro):
        with open(ficheiro, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def proximo_id(dados: dict) -> int:
    if not dados:
        return 1
    return max(int(k) for k in dados.keys()) + 1
    Carrega um dicionário de um ficheiro JSON.
    Devolve {} se o ficheiro não existir.
    """
    if os.path.exists(ficheiro):
        with open(ficheiro, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
