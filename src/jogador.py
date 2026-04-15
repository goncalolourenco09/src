jogadores = []
ultimo_id = 0


def gerar_id():
    global ultimo_id
    ultimo_id += 1
    return ultimo_id


# ------------------------
# VALIDAÇÕES
# ------------------------
def camisola_existe(numero):
    return any(j["numero_camisa"] == numero for j in jogadores)


# ------------------------
# CRIAR
# ------------------------
def criar_jogador(nome, data_nascimento, numero, posicao, salario):
    print("\n--- Adicionar Jogador ---")

    if camisola_existe(numero):
        return 409, "Conflito - Camisola já usada!"

    if salario < 0:
        return 400, "Salário inválido!"

    jogador = {
        "id_jogador": gerar_id(),
        "nome": nome,
        "data_nascimento": data_nascimento,
        "posicao": posicao,
        "numero_camisa": numero,
        "salario": salario
    }

    jogadores.append(jogador)
    return 201, jogador


# ------------------------
# LISTAR TODOS
# ------------------------
def listar_jogadores():
    if len(jogadores) == 0:
        return 204, "Sem jogadores registados"
    return 200, jogadores


# ------------------------
# OBTER UM
# ------------------------
def obter_jogador(id_jogador):
    for j in jogadores:
        if j["id_jogador"] == id_jogador:
            return 200, j
    return 404, "Jogador não encontrado"


# ------------------------
# ATUALIZAR
# ------------------------
def atualizar_jogador_service(id_jogador, nome=None, numero=None):
    for j in jogadores:
        if j["id_jogador"] == id_jogador:

            if nome:
                j["nome"] = nome

            if numero:
                if camisola_existe(numero):
                    return 409, "Número de camisola já usado!"
                j["numero_camisa"] = numero

            return 200, j

    return 404, "Jogador não encontrado"


# ------------------------
# REMOVER
# ------------------------
def remover_jogador_service(id_jogador):
    for j in jogadores:
        if j["id_jogador"] == id_jogador:
            jogadores.remove(j)
            return 200, j

    return 404, "Jogador não encontrado"
