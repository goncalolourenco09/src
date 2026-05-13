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
        return 500, "Nome inválido."
    if not validar_data(data_nascimento):
        return 500, "Data inválida. Utilize o formato YYYY-MM-DD."
    if not validar_numero_camisola(numero_camisa):
        return 500, "Número de camisola inválido."
    if not validar_posicao(posicao):
        return 500, "Posição inválida."
    if not validar_salario(salario):
        return 500, "Salário inválido."
    for id_j, j in jogadores.items():
        if j["numero_camisa"] == numero_camisa:
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
    return 201, jogador

# ==========================
# READ ALL
# ==========================

def listar_jogadores():
    carregar_jogadores()
    if not jogadores:
        return 404, "Não existem jogadores registados."
    return 200, jogadores

# ==========================
# READ ONE
# ==========================

def consultar_jogador(id_jogador):
    carregar_jogadores()
    if id_jogador not in jogadores:
        return 404, "Jogador não encontrado."
    return 200, jogadores[id_jogador]

# ==========================
# UPDATE
# ==========================

def atualizar_jogador(id_jogador, nome=None, numero_camisa=None, salario=None, posicao=None):
    carregar_jogadores()
    if id_jogador not in jogadores:
        return 404, "Jogador não encontrado."
    if nome:
        if not validar_nome(nome):
            return 500, "Nome inválido."
        jogadores[id_jogador]["nome"] = nome
    if numero_camisa:
        if not validar_numero_camisola(numero_camisa):
            return 500, "Número de camisola inválido."
        for id_j, j in jogadores.items():
            if j["numero_camisa"] == numero_camisa and id_j != id_jogador:
                return 409, f"Já existe um jogador com a camisola {numero_camisa}."
        jogadores[id_jogador]["numero_camisa"] = numero_camisa
    if salario:
        if not validar_salario(salario):
            return 500, "Salário inválido."
        jogadores[id_jogador]["salario"] = salario
    if posicao:
        if not validar_posicao(posicao):
            return 500, "Posição inválida."
        jogadores[id_jogador]["posicao"] = posicao
    guardar_jogadores()
    return 200, jogadores[id_jogador]

# ==========================
# DELETE
# ==========================

def remover_jogador(id_jogador):
    carregar_jogadores()
    if id_jogador not in jogadores:
        return 404, "Jogador não encontrado."
    del jogadores[id_jogador]
    guardar_jogadores()
    return 200, id_jogador
