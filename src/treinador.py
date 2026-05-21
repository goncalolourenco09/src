from logger import get_logger
from utils import (
    gerar_id_treinador,
    validar_nome,
    validar_data,
    validar_licenca_UEFA,
)
from persistencia import guardar, carregar, FICHEIRO_TREINADORES

logger = get_logger(__name__)

treinadores = {}

# ==========================
# Persistência
# ==========================

def guardar_treinadores():
    guardar(FICHEIRO_TREINADORES, treinadores)

def carregar_treinadores():
    global treinadores
    treinadores = carregar(FICHEIRO_TREINADORES)

# ==========================
# CREATE
# ==========================

def criar_treinador(nome, nacionalidade, data_nascimento, licenca_UEFA, id_clube=None):
    carregar_treinadores()

    if not validar_nome(nome):
        logger.error("Erro ao criar treinador: nome inválido — '%s'", nome)
        return 500, "Nome inválido."
    if not validar_nome(nacionalidade):
        logger.error("Erro ao criar treinador: nacionalidade inválida — '%s'", nacionalidade)
        return 500, "Nacionalidade inválida."
    if not validar_data(data_nascimento):
        logger.error("Erro ao criar treinador: data inválida — '%s'", data_nascimento)
        return 500, "Data inválida. Utilize o formato YYYY-MM-DD."
    if not validar_licenca_UEFA(licenca_UEFA):
        logger.error("Erro ao criar treinador: licença UEFA inválida — '%s'", licenca_UEFA)
        return 500, "Licença UEFA inválida."
    if id_clube is not None:
        if not isinstance(id_clube, int) or id_clube <= 0:
            logger.error("Erro ao criar treinador: ID de clube inválido — %s", id_clube)
            return 500, "ID de clube inválido."

    id_treinador = gerar_id_treinador()
    treinador = {
        "nome": nome,
        "nacionalidade": nacionalidade,
        "data_nascimento": data_nascimento,
        "licenca_UEFA": licenca_UEFA.upper(),
        "id_clube": id_clube
    }
    treinadores[id_treinador] = treinador
    guardar_treinadores()
    logger.info("Treinador criado: '%s' | licença %s | clube ID %s", nome, licenca_UEFA.upper(), id_clube)
    return 201, treinador

# ==========================
# READ ALL
# ==========================

def listar_treinadores():
    carregar_treinadores()
    if not treinadores:
        logger.error("Listagem de treinadores: nenhum treinador registado")
        return 404, "Não existem treinadores registados."
    logger.info("Listagem de treinadores: %d treinador(es) encontrado(s)", len(treinadores))
    return 200, treinadores

# ==========================
# READ ONE
# ==========================

def consultar_treinador(id_treinador):
    carregar_treinadores()
    if id_treinador not in treinadores:
        logger.error("Treinador com ID %s não encontrado", id_treinador)
        return 404, "Treinador não encontrado."
    logger.info("Treinador consultado: ID %s — '%s'", id_treinador, treinadores[id_treinador]["nome"])
    return 200, treinadores[id_treinador]

# ==========================
# UPDATE
# ==========================

def atualizar_treinador(id_treinador, nome=None, nacionalidade=None, licenca_UEFA=None, id_clube=None):
    carregar_treinadores()
    if id_treinador not in treinadores:
        logger.error("Atualização falhada: treinador com ID %s não encontrado", id_treinador)
        return 404, "Treinador não encontrado."

    if nome:
        if not validar_nome(nome):
            logger.error("Atualização falhada: nome inválido — '%s'", nome)
            return 500, "Nome inválido."
        treinadores[id_treinador]["nome"] = nome

    if nacionalidade:
        if not validar_nome(nacionalidade):
            logger.error("Atualização falhada: nacionalidade inválida — '%s'", nacionalidade)
            return 500, "Nacionalidade inválida."
        treinadores[id_treinador]["nacionalidade"] = nacionalidade

    if licenca_UEFA:
        if not validar_licenca_UEFA(licenca_UEFA):
            logger.error("Atualização falhada: licença UEFA inválida — '%s'", licenca_UEFA)
            return 500, "Licença UEFA inválida."
        treinadores[id_treinador]["licenca_UEFA"] = licenca_UEFA.upper()

    if id_clube:
        if not isinstance(id_clube, int) or id_clube <= 0:
            logger.error("Atualização falhada: ID de clube inválido — %s", id_clube)
            return 500, "ID de clube inválido."
        treinadores[id_treinador]["id_clube"] = id_clube

    guardar_treinadores()
    logger.info("Treinador atualizado: ID %s — '%s'", id_treinador, treinadores[id_treinador]["nome"])
    return 200, treinadores[id_treinador]

# ==========================
# DELETE
# ==========================

def remover_treinador(id_treinador):
    carregar_treinadores()
    if id_treinador not in treinadores:
        logger.error("Remoção falhada: treinador com ID %s não encontrado", id_treinador)
        return 404, "Treinador não encontrado."
    nome = treinadores[id_treinador]["nome"]
    del treinadores[id_treinador]
    guardar_treinadores()
    logger.info("Treinador removido: ID %s — '%s'", id_treinador, nome)
    return 200, id_treinador
