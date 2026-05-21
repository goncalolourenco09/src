from logger import get_logger
from utils import gerar_id_clube, validar_nome, validar_nif
from persistencia import guardar, carregar, FICHEIRO_CLUBES

logger = get_logger(__name__)

clubes = {}

# ==========================
# Persistência
# ==========================

def guardar_clubes():
    guardar(FICHEIRO_CLUBES, clubes)

def carregar_clubes():
    global clubes
    clubes = carregar(FICHEIRO_CLUBES)

# ==========================
# CREATE
# ==========================

def criar_clube(nome, nif):
    carregar_clubes()

    if not validar_nome(nome):
        logger.error("Erro ao criar clube: nome inválido — '%s'", nome)
        return 500, "Nome inválido."
    if not validar_nif(nif):
        logger.error("Erro ao criar clube: NIF inválido — '%s'", nif)
        return 500, "NIF inválido."

    for id_c, c in clubes.items():
        if c["nif"] == nif:
            logger.error("NIF '%s' já está registado no clube '%s'", nif, c["nome"])
            return 409, "Já existe um clube com este NIF."

    id_clube = gerar_id_clube()
    clube = {
        "nome": nome,
        "nif": nif
    }
    clubes[id_clube] = clube
    guardar_clubes()
    logger.info("Clube criado: '%s' | NIF %s", nome, nif)
    return 201, clube

# ==========================
# READ ALL
# ==========================

def listar_clubes():
    carregar_clubes()
    if not clubes:
        logger.error("Listagem de clubes: nenhum clube registado")
        return 404, "Não existem clubes registados."
    logger.info("Listagem de clubes: %d clube(s) encontrado(s)", len(clubes))
    return 200, clubes

# ==========================
# READ ONE
# ==========================

def consultar_clube(id_clube):
    carregar_clubes()
    if id_clube not in clubes:
        logger.error("Clube com ID %s não encontrado", id_clube)
        return 404, "Clube não encontrado."
    logger.info("Clube consultado: ID %s — '%s'", id_clube, clubes[id_clube]["nome"])
    return 200, clubes[id_clube]

# ==========================
# UPDATE
# ==========================

def atualizar_clube(id_clube, nome=None, nif=None):
    carregar_clubes()
    if id_clube not in clubes:
        logger.error("Atualização falhada: clube com ID %s não encontrado", id_clube)
        return 404, "Clube não encontrado."

    if nome:
        if not validar_nome(nome):
            logger.error("Atualização falhada: nome inválido — '%s'", nome)
            return 500, "Nome inválido."
        clubes[id_clube]["nome"] = nome

    if nif:
        if not validar_nif(nif):
            logger.error("Atualização falhada: NIF inválido — '%s'", nif)
            return 500, "NIF inválido."
        for id_c, c in clubes.items():
            if c["nif"] == nif and id_c != id_clube:
                logger.error("Atualização falhada: NIF '%s' já está registado no clube '%s'", nif, c["nome"])
                return 409, "Já existe um clube com este NIF."
        clubes[id_clube]["nif"] = nif

    guardar_clubes()
    logger.info("Clube atualizado: ID %s — '%s'", id_clube, clubes[id_clube]["nome"])
    return 200, clubes[id_clube]

# ==========================
# DELETE
# ==========================

def remover_clube(id_clube):
    carregar_clubes()
    if id_clube not in clubes:
        logger.error("Remoção falhada: clube com ID %s não encontrado", id_clube)
        return 404, "Clube não encontrado."
    nome = clubes[id_clube]["nome"]
    del clubes[id_clube]
    guardar_clubes()
    logger.info("Clube removido: ID %s — '%s'", id_clube, nome)
    return 200, id_clube
