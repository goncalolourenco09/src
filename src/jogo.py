from utils import (
    gerar_id_jogo,
    validar_nome,
    validar_data,
    validar_golos,
)

jogos = {}

# ==========================
# CREATE
# ==========================

def criar_jogo(data, estadio, id_clube_casa, id_clube_fora, golos_casa=0, golos_fora=0):
    if not validar_data(data):
        return 500, "Data inválida. Utilize o formato YYYY-MM-DD."
    if not validar_nome(estadio):
        return 500, "Nome do estádio inválido."
    if not isinstance(id_clube_casa, int) or id_clube_casa <= 0:
        return 500, "ID do clube da casa inválido."
    if not isinstance(id_clube_fora, int) or id_clube_fora <= 0:
        return 500, "ID do clube visitante inválido."
    if id_clube_casa == id_clube_fora:
        return 500, "Os dois clubes não podem ser o mesmo."
    if not validar_golos(golos_casa):
        return 500, "Golos da casa inválidos."
    if not validar_golos(golos_fora):
        return 500, "Golos de fora inválidos."
    id_jogo = gerar_id_jogo()
    jogo = {
        "data": data,
        "estadio": estadio,
        "id_clube_casa": id_clube_casa,
        "id_clube_fora": id_clube_fora,
        "golos_casa": golos_casa,
        "golos_fora": golos_fora,
        "marcadores": [],
        "convocados": []
    }
    jogos[id_jogo] = jogo
    return 201, jogo

# ==========================
# READ ALL
# ==========================

def listar_jogos():
    if not jogos:
        return 404, "Não existem jogos registados."
    return 200, jogos

# ==========================
# READ ONE
# ==========================

def consultar_jogo(id_jogo):
    if id_jogo not in jogos:
        return 404, "Jogo não encontrado."
    return 200, jogos[id_jogo]

# ==========================
# UPDATE
# ==========================

def atualizar_jogo(id_jogo, golos_casa=None, golos_fora=None, estadio=None):
    if id_jogo not in jogos:
        return 404, "Jogo não encontrado."
    if golos_casa is not None:
        if not validar_golos(golos_casa):
            return 500, "Golos da casa inválidos."
        jogos[id_jogo]["golos_casa"] = golos_casa
    if golos_fora is not None:
        if not validar_golos(golos_fora):
            return 500, "Golos de fora inválidos."
        jogos[id_jogo]["golos_fora"] = golos_fora
    if estadio:
        if not validar_nome(estadio):
            return 500, "Nome do estádio inválido."
        jogos[id_jogo]["estadio"] = estadio
    return 200, jogos[id_jogo]

# ==========================
# DELETE
# ==========================

def remover_jogo(id_jogo):
    if id_jogo not in jogos:
        return 404, "Jogo não encontrado."
    del jogos[id_jogo]
    return 200, id_jogo
