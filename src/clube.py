from utils import gerar_id_clube, validar_nome, validar_nif

clubes = {}

# ==========================
# CREATE
# ==========================

def criar_clube(nome, nif):
    if not validar_nome(nome):
        return 500, "Nome inválido."
    if not validar_nif(nif):
        return 500, "NIF inválido."
    for id_c, c in clubes.items():
        if c["nif"] == nif:
            return 409, "Já existe um clube com este NIF."
    id_clube = gerar_id_clube()
    clube = {
        "nome": nome,
        "nif": nif
    }
    clubes[id_clube] = clube
    return 201, clube

# ==========================
# READ ALL
# ==========================

def listar_clubes():
    if not clubes:
        return 404, "Não existem clubes registados."
    return 200, clubes

# ==========================
# READ ONE
# ==========================

def consultar_clube(id_clube):
    if id_clube not in clubes:
        return 404, "Clube não encontrado."
    return 200, clubes[id_clube]

# ==========================
# UPDATE
# ==========================

def atualizar_clube(id_clube, nome=None, nif=None):
    if id_clube not in clubes:
        return 404, "Clube não encontrado."
    if nome:
        if not validar_nome(nome):
            return 500, "Nome inválido."
        clubes[id_clube]["nome"] = nome
    if nif:
        if not validar_nif(nif):
            return 500, "NIF inválido."
        for id_c, c in clubes.items():
            if c["nif"] == nif and id_c != id_clube:
                return 409, "Já existe um clube com este NIF."
        clubes[id_clube]["nif"] = nif
    return 200, clubes[id_clube]

# ==========================
# DELETE
# ==========================

def remover_clube(id_clube):
    if id_clube not in clubes:
        return 404, "Clube não encontrado."
    del clubes[id_clube]
    return 200, id_clube
