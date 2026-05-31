from persistencia import carregar, guardar, FICHEIROS, proximo_id

def validar_nome(nome: str) -> bool:
    return isinstance(nome, str) and len(nome.strip()) >= 2

def validar_nif(nif) -> bool:
    nif_str = str(nif).strip()
    return nif_str.isdigit() and len(nif_str) == 9

# ====================== CRUD CLUBES ======================
def criar_clube(nome: str, nif):
    if not validar_nome(nome):
        return False, "Nome inválido (mínimo 2 caracteres)"
    if not validar_nif(nif):
        return False, "NIF inválido (deve ter 9 dígitos)"

    clubes = carregar(FICHEIROS["clubes"])
    if any(c["nif"] == str(nif) for c in clubes.values()):
        return False, "Já existe um clube com este NIF"

    novo_id = str(proximo_id(clubes))
    clubes[novo_id] = {"nome": nome.strip(), "nif": str(nif)}
    guardar(FICHEIROS["clubes"], clubes)
    return True, novo_id

def listar_clubes():
    return carregar(FICHEIROS["clubes"])

def atualizar_clube(id_clube: str, nome=None, nif=None):
    clubes = listar_clubes()
    if id_clube not in clubes:
        return False, "Clube não encontrado"

    if nome:
        if not validar_nome(nome):
            return False, "Nome inválido"
        clubes[id_clube]["nome"] = nome.strip()
    if nif:
        if not validar_nif(nif):
            return False, "NIF inválido"
        clubes[id_clube]["nif"] = str(nif)

    guardar(FICHEIROS["clubes"], clubes)
    return True, "Clube atualizado com sucesso"

def remover_clube(id_clube: str):
    clubes = listar_clubes()
    if id_clube not in clubes:
        return False, "Clube não encontrado"
    del clubes[id_clube]
    guardar(FICHEIROS["clubes"], clubes)
    return True, "Clube removido"
