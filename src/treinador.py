from persistencia import carregar, guardar, FICHEIROS, proximo_id

def validar_nome(nome: str) -> bool:
    return isinstance(nome, str) and len(nome.strip()) >= 2

def validar_licenca(licenca: str) -> bool:
    return licenca.upper() in ["A", "B", "PRO"]

def criar_treinador(nome: str, nacionalidade: str, data_nasc: str, licenca: str, id_clube=None):
    if not validar_nome(nome):
        return False, "Nome inválido"
    if not validar_nome(nacionalidade):
        return False, "Nacionalidade inválida"
    if not validar_licenca(licenca):
        return False, "Licença inválida (A, B ou PRO)"

    treinadores = carregar(FICHEIROS["treinadores"])
    novo_id = str(proximo_id(treinadores))

    treinadores[novo_id] = {
        "nome": nome.strip(),
        "nacionalidade": nacionalidade.strip(),
        "data_nascimento": data_nasc,
        "licenca_UEFA": licenca.upper(),
        "id_clube": id_clube
    }
    guardar(FICHEIROS["treinadores"], treinadores)
    return True, novo_id

def listar_treinadores():
    return carregar(FICHEIROS["treinadores"])

def remover_treinador(id_treinador: str):
    treinadores = listar_treinadores()
    if id_treinador not in treinadores:
        return False, "Treinador não encontrado"
    del treinadores[id_treinador]
    guardar(FICHEIROS["treinadores"], treinadores)
    return True, "Treinador removido"
