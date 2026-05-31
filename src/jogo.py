from persistencia import carregar, guardar, FICHEIROS, proximo_id

def criar_jogo(data: str, estadio: str, id_casa: int, id_fora: int, golos_casa=0, golos_fora=0):
    if not validar_nome(estadio):
        return False, "Nome do estádio inválido"
    if id_casa == id_fora:
        return False, "Os clubes não podem ser o mesmo"

    jogos = carregar(FICHEIROS["jogos"])
    novo_id = str(proximo_id(jogos))

    jogos[novo_id] = {
        "data": data,
        "estadio": estadio.strip(),
        "id_clube_casa": id_casa,
        "id_clube_fora": id_fora,
        "golos_casa": int(golos_casa),
        "golos_fora": int(golos_fora)
    }
    guardar(FICHEIROS["jogos"], jogos)
    return True, novo_id

def listar_jogos():
    return carregar(FICHEIROS["jogos"])

def remover_jogo(id_jogo: str):
    jogos = listar_jogos()
    if id_jogo not in jogos:
        return False, "Jogo não encontrado"
    del jogos[id_jogo]
    guardar(FICHEIROS["jogos"], jogos)
    return True, "Jogo removido"
