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
def atualizar_jogador(id_jogador, nome=None, numero=None, salario=None, posicao=None):
    for j in jogadores:
        if j["id_jogador"] == id_jogador:

            if nome is not None:
                j["nome"] = nome

            while True:
                try:
                    salario = float(input("Salário: ").replace(",", "."))
                    break
                except ValueError:
                    print("Erro: digite um salário válido (ex: 1500.50)")

            while True:
                try:
                    numero = int(input("Número da camisola: "))
                    break
                except ValueError:
                    print(" Por favor, digite um número válido!")

            if posicao is not None:
                j["posicao"] = posicao

            return 200, j

    return 404, "Jogador não encontrado"

# ------------------------
# REMOVER
# ------------------------
def remover_jogador(id_jogador):
    for j in jogadores:
        if j["id_jogador"] == id_jogador:
            jogadores.remove(j)
            return 200, j

    return 404, "Jogador não encontrado"