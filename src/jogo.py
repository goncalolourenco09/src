import os


def criar_jogo(data, estadio, id_clube_casa, id_clube_fora, golos_casa=0, golos_fora=0):
    novo_id = 1 if not jogos else jogos[-1]["id_jogo"] + 1
    novo = {
        "id_jogo": novo_id,
        "data": data,
        "estadio": estadio,
        "id_clube_casa": id_clube_casa,
        "id_clube_fora": id_clube_fora,
        "golos_casa": golos_casa,
        "golos_fora": golos_fora,
    }
    jogos.append(novo)
    return 201, novo


def listar_jogos():
    if not jogos:
        return 200, "Nenhum jogo encontrado."
    return 200, jogos


def obter_jogo(id_jogo):
    for j in jogos:
        if j["id_jogo"] == id_jogo:
            return 200, j
    return 404, "Jogo não encontrado."


def atualizar_jogo(id_jogo, golos_casa=None, golos_fora=None, estadio=None):
    for j in jogos:
        if j["id_jogo"] == id_jogo:
            if golos_casa is not None:
                j["golos_casa"] = golos_casa
            if golos_fora is not None:
                j["golos_fora"] = golos_fora
            if estadio:
                j["estadio"] = estadio
            return 200, j
    return 404, "Jogo não encontrado."


def remover_jogo(id_jogo):
    jogos = carregar_jogos()
    for j in jogos:
        if j["id_jogo"] == id_jogo:
            jogos.remove(j)
            return 200, j
    return 404, "Jogo não encontrado."