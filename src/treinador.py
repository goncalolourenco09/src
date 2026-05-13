from utils import (
    gerar_id_treinador,
    validar_nome,
    validar_data,
    validar_licenca_UEFA,
)

treinadores = {}

# ==========================
# CREATE
# ==========================

def criar_treinador(nome, nacionalidade, data_nascimento, licenca_UEFA, id_clube=None):
    if not validar_nome(nome):
        return 500, "Nome inválido."
    if not validar_nome(nacionalidade):
        return 500, "Nacionalidade inválida."
    if not validar_data(data_nascimento):
        return 500, "Data inválida. Utilize o formato YYYY-MM-DD."
    if not validar_licenca_UEFA(licenca_UEFA):
        return 500, "Licença UEFA inválida."
    if id_clube is not None:
        if not isinstance(id_clube, int) or id_clube <= 0:
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
    return 201, treinador

# ==========================
# READ ALL
# ==========================

def listar_treinadores():
    if not treinadores:
        return 404, "Não existem treinadores registados."
    return 200, treinadores

# ==========================
# READ ONE
# ==========================

def consultar_treinador(id_treinador):
    if id_treinador not in treinadores:
        return 404, "Treinador não encontrado."
    return 200, treinadores[id_treinador]

# ==========================
# UPDATE
# ==========================

def atualizar_treinador(id_treinador, nome=None, nacionalidade=None, licenca_UEFA=None, id_clube=None):
    if id_treinador not in treinadores:
        return 404, "Treinador não encontrado."
    if nome:
        if not validar_nome(nome):
            return 500, "Nome inválido."
        treinadores[id_treinador]["nome"] = nome
    if nacionalidade:
        if not validar_nome(nacionalidade):
            return 500, "Nacionalidade inválida."
        treinadores[id_treinador]["nacionalidade"] = nacionalidade
    if licenca_UEFA:
        if not validar_licenca_UEFA(licenca_UEFA):
            return 500, "Licença UEFA inválida."
        treinadores[id_treinador]["licenca_UEFA"] = licenca_UEFA.upper()
    if id_clube:
        if not isinstance(id_clube, int) or id_clube <= 0:
            return 500, "ID de clube inválido."
        treinadores[id_treinador]["id_clube"] = id_clube
    return 200, treinadores[id_treinador]

# ==========================
# DELETE
# ==========================

def remover_treinador(id_treinador):
    if id_treinador not in treinadores:
        return 404, "Treinador não encontrado."
    del treinadores[id_treinador]
    return 200, id_treinador
