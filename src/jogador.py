import logging
from utils import (
    gerar_id_jogador,
    validar_nome,
    validar_data,
    validar_salario,
    validar_numero_camisola,
    validar_posicao,
    calcular_idade,
)
from persistencia import guardar, carregar, FICHEIRO_JOGADORES

logger = logging.getLogger(__name__)

jogadores = {}

# ==========================
# Persistência
# ==========================

def guardar_jogadores():
    guardar(FICHEIRO_JOGADORES, jogadores)

def carregar_jogadores():
    global jogadores
    jogadores = carregar(FICHEIRO_JOGADORES)

# ==========================
# CREATE
# ==========================

def criar_jogador(nome, data_nascimento, numero_camisa, posicao, salario):
    carregar_jogadores()

    if not validar_nome(nome):
        logger.error("Erro ao criar jogador: nome inválido — '%s'", nome)
        return 500, "Nome inválido."
    if not validar_data(data_nascimento):
        logger.error("Erro ao criar jogador: data inválida — '%s'", data_nascimento)
        return 500, "Data inválida. Utilize o formato YYYY-MM-DD."
    if not validar_numero_camisola(numero_camisa):
        logger.error("Erro ao criar jogador: número de camisola inválido — %s", numero_camisa)
        return 500, "Número de camisola inválido."
    if not validar_posicao(posicao):
        logger.error("Erro ao criar jogador: posição inválida — '%s'", posicao)
        return 500, "Posição inválida."
    if not validar_salario(salario):
        logger.error("Erro ao criar jogador: salário inválido — %s", salario)
        return 500, "Salário inválido."

    for id_j, j in jogadores.items():
        if j["numero_camisa"] == numero_camisa:
            logger.warning("Camisola %s já está atribuída ao jogador '%s'", numero_camisa, j["nome"])
            return 409, f"Já existe um jogador com a camisola {numero_camisa}."

    id_jogador = gerar_id_jogador()
    jogador = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "idade": calcular_idade(data_nascimento),
        "posicao": posicao,
        "numero_camisa": numero_camisa,
        "salario": salario
    }
    jogadores[id_jogador] = jogador
    guardar_jogadores()
    logger.info("Jogador criado: '%s' | camisola %s | posição %s", nome, numero_camisa, posicao)
    return 201, jogador

# ==========================
# READ ALL
# ==========================

def listar_jogadores():
    carregar_jogadores()
    if not jogadores:
        logger.warning("Listagem de jogadores: nenhum jogador registado")
        return 404, "Não existem jogadores registados."
    logger.info("Listagem de jogadores: %d jogador(es) encontrado(s)", len(jogadores))
    return 200, jogadores

# ==========================
# READ ONE
# ==========================

def consultar_jogador(id_jogador):
    carregar_jogadores()
    if id_jogador not in jogadores:
        logger.warning("Jogador com ID %s não encontrado", id_jogador)
        return 404, "Jogador não encontrado."
    logger.info("Jogador consultado: ID %s — '%s'", id_jogador, jogadores[id_jogador]["nome"])
    return 200, jogadores[id_jogador]

# ==========================
# UPDATE
# ==========================

def atualizar_jogador(id_jogador, nome=None, numero_camisa=None, salario=None, posicao=None):
    carregar_jogadores()
    if id_jogador not in jogadores:
        logger.warning("Atualização falhada: jogador com ID %s não encontrado", id_jogador)
        return 404, "Jogador não encontrado."

    if nome:
        if not validar_nome(nome):
            logger.error("Atualização falhada: nome inválido — '%s'", nome)
            return 500, "Nome inválido."
        jogadores[id_jogador]["nome"] = nome

    if numero_camisa:
        if not validar_numero_camisola(numero_camisa):
            logger.error("Atualização falhada: número de camisola inválido — %s", numero_camisa)
            return 500, "Número de camisola inválido."
        for id_j, j in jogadores.items():
            if j["numero_camisa"] == numero_camisa and id_j != id_jogador:
                logger.warning("Atualização falhada: camisola %s já está atribuída ao jogador '%s'", numero_camisa, j["nome"])
                return 409, f"Já existe um jogador com a camisola {numero_camisa}."
        jogadores[id_jogador]["numero_camisa"] = numero_camisa

    if salario:
        if not validar_salario(salario):
            logger.error("Atualização falhada: salário inválido — %s", salario)
            return 500, "Salário inválido."
        jogadores[id_jogador]["salario"] = salario

    if posicao:
        if not validar_posicao(posicao):
            logger.error("Atualização falhada: posição inválida — '%s'", posicao)
            return 500, "Posição inválida."
        jogadores[id_jogador]["posicao"] = posicao

    guardar_jogadores()
    logger.info("Jogador atualizado: ID %s — '%s'", id_jogador, jogadores[id_jogador]["nome"])
    return 200, jogadores[id_jogador]

# ==========================
# DELETE
# ==========================

def remover_jogador(id_jogador):
    carregar_jogadores()
    if id_jogador not in jogadores:
        logger.warning("Remoção falhada: jogador com ID %s não encontrado", id_jogador)
        return 404, "Jogador não encontrado."
    nome = jogadores[id_jogador]["nome"]
    del jogadores[id_jogador]
    guardar_jogadores()
    logger.info("Jogador removido: ID %s — '%s'", id_jogador, nome)
    return 200, id_jogador
