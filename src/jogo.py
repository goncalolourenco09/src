from utils import (
    gerar_id_jogo,
    validar_nome,
    validar_data,
    validar_golos,
)
from persistencia import guardar, carregar, FICHEIRO_JOGOS

jogos = {}

# ==========================
# Persistência
# ==========================

def guardar_jogos():
    guardar(FICHEIRO_JOGOS, jogos)

def carregar_jogos():
    global jogos
    jogos = carregar(FICHEIRO_JOGOS)

# ==========================
# CREATE
# ==========================

def criar_jogo(data, estadio, id_clube_casa, id_clube_fora, golos_casa=0, golos_fora=0):
    carregar_jogos()

    if not validar_data(data):
        logger.error("Erro ao criar jogo: data inválida — '%s'", data)
        return 500, "Data inválida. Utilize o formato YYYY-MM-DD."
    if not validar_nome(estadio):
        logger.error("Erro ao criar jogo: nome do estádio inválido — '%s'", estadio)
        return 500, "Nome do estádio inválido."
    if not isinstance(id_clube_casa, int) or id_clube_casa <= 0:
        logger.error("Erro ao criar jogo: ID do clube da casa inválido — %s", id_clube_casa)
        return 500, "ID do clube da casa inválido."
    if not isinstance(id_clube_fora, int) or id_clube_fora <= 0:
        logger.error("Erro ao criar jogo: ID do clube visitante inválido — %s", id_clube_fora)
        return 500, "ID do clube visitante inválido."
    if id_clube_casa == id_clube_fora:
        logger.error("Erro ao criar jogo: clube da casa e visitante são o mesmo (ID %s)", id_clube_casa)
        return 500, "Os dois clubes não podem ser o mesmo."
    if not validar_golos(golos_casa):
        logger.error("Erro ao criar jogo: golos da casa inválidos — %s", golos_casa)
        return 500, "Golos da casa inválidos."
    if not validar_golos(golos_fora):
        logger.error("Erro ao criar jogo: golos de fora inválidos — %s", golos_fora)
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
    guardar_jogos()
    logger.info("Jogo criado: ID %s | %s | %s | %d-%d", id_jogo, data, estadio, golos_casa, golos_fora)
    return 201, jogo

# ==========================
# READ ALL
# ==========================

def listar_jogos():
    carregar_jogos()
    if not jogos:
        logger.error("Listagem de jogos: nenhum jogo registado")
        return 404, "Não existem jogos registados."
    logger.info("Listagem de jogos: %d jogo(s) encontrado(s)", len(jogos))
    return 200, jogos

# ==========================
# READ ONE
# ==========================

def consultar_jogo(id_jogo):
    carregar_jogos()
    if id_jogo not in jogos:
        logger.error("Jogo com ID %s não encontrado", id_jogo)
        return 404, "Jogo não encontrado."
    logger.info("Jogo consultado: ID %s | %s | %s", id_jogo, jogos[id_jogo]["data"], jogos[id_jogo]["estadio"])
    return 200, jogos[id_jogo]

# ==========================
# UPDATE
# ==========================

def atualizar_jogo(id_jogo, golos_casa=None, golos_fora=None, estadio=None):
    carregar_jogos()
    if id_jogo not in jogos:
        logger.error("Atualização falhada: jogo com ID %s não encontrado", id_jogo)
        return 404, "Jogo não encontrado."

    if golos_casa is not None:
        if not validar_golos(golos_casa):
            logger.error("Atualização falhada: golos da casa inválidos — %s", golos_casa)
            return 500, "Golos da casa inválidos."
        jogos[id_jogo]["golos_casa"] = golos_casa

    if golos_fora is not None:
        if not validar_golos(golos_fora):
            logger.error("Atualização falhada: golos de fora inválidos — %s", golos_fora)
            return 500, "Golos de fora inválidos."
        jogos[id_jogo]["golos_fora"] = golos_fora

    if estadio:
        if not validar_nome(estadio):
            logger.error("Atualização falhada: nome do estádio inválido — '%s'", estadio)
            return 500, "Nome do estádio inválido."
        jogos[id_jogo]["estadio"] = estadio

    guardar_jogos()
    logger.info("Jogo atualizado: ID %s | resultado %d-%d", id_jogo, jogos[id_jogo]["golos_casa"], jogos[id_jogo]["golos_fora"])
    return 200, jogos[id_jogo]

# ==========================
# DELETE
# ==========================

def remover_jogo(id_jogo):
    carregar_jogos()
    if id_jogo not in jogos:
        logger.error("Remoção falhada: jogo com ID %s não encontrado", id_jogo)
        return 404, "Jogo não encontrado."
    estadio = jogos[id_jogo]["estadio"]
    data = jogos[id_jogo]["data"]
    del jogos[id_jogo]
    guardar_jogos()
    logger.info("Jogo removido: ID %s | %s | %s", id_jogo, data, estadio)
    return 200, id_jogo
