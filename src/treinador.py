import os

treinadores = []

def criar_treinador(nome, nacionalidade, data_nascimento, licenca_UEFA, id_clube=None):
    novo_id = 1 if not treinadores else treinadores[-1]["id_treinador"] + 1
    novo = {
        "id_treinador": novo_id,
        "nome": nome,
        "nacionalidade": nacionalidade,
        "data_nascimento": data_nascimento,
        "licenca_UEFA": licenca_UEFA,
        "id_clube": id_clube,
    }
    treinadores.append(novo)
    return 201, novo


def listar_treinadores():
    if not treinadores:
        return 200, "Nenhum treinador encontrado."
    return 200, treinadores


def obter_treinador(id_treinador):
    for t in treinadores:
        if t["id_treinador"] == id_treinador:
            return 200, t
    return 404, "Treinador não encontrado."


def atualizar_treinador(id_treinador, nome=None, nacionalidade=None, licenca_UEFA=None, id_clube=None):
    for t in treinadores:
        if t["id_treinador"] == id_treinador:
            if nome:
                t["nome"] = nome
            if nacionalidade:
                t["nacionalidade"] = nacionalidade
            if licenca_UEFA:
                t["licenca_UEFA"] = licenca_UEFA
            if id_clube is not None:
                t["id_clube"] = id_clube
            return 200, t
    return 404, "Treinador não encontrado."


def remover_treinador(id_treinador):
    for t in treinadores:
        if t["id_treinador"] == id_treinador:
            treinadores.remove(t)
            return 200, t
    return 404, "Treinador não encontrado."
