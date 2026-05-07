from utils import (
    validar_nome,
    validar_data,
    validar_golos,
    gerar_id_de_lista,
)

# ============================================================
# DADOS EM MEMÓRIA
# ============================================================

jogos = []   # lista principal que guarda todos os jogos


# ============================================================
# CRIAR
# ============================================================

def criar_jogo(data, estadio, id_clube_casa, id_clube_fora, golos_casa=0, golos_fora=0):
    """
    Cria um novo jogo após validar os campos obrigatórios.

    Args:
        data (str): data do jogo no formato "YYYY-MM-DD"
        estadio (str): nome do estádio onde se realiza o jogo
        id_clube_casa (int): ID do clube da casa
        id_clube_fora (int): ID do clube visitante
        golos_casa (int): golos da equipa da casa (padrão 0)
        golos_fora (int): golos da equipa visitante (padrão 0)

    Returns:
        tuple: (201, jogo criado) ou (400, mensagem de erro)
    """
    # Validar data
    ok, erro = validar_data(data)
    if not ok:
        return 400, erro

    # Validar nome do estádio
    ok, erro = validar_nome(estadio)
    if not ok:
        return 400, f"Estádio inválido: {erro}"

    # Validar IDs dos clubes
    if not isinstance(id_clube_casa, int) or id_clube_casa <= 0:
        return 400, "ID do clube da casa inválido."
    if not isinstance(id_clube_fora, int) or id_clube_fora <= 0:
        return 400, "ID do clube visitante inválido."
    if id_clube_casa == id_clube_fora:
        return 400, "Os dois clubes não podem ser o mesmo."

    # Validar golos
    ok, erro = validar_golos(golos_casa)
    if not ok:
        return 400, f"Golos da casa inválidos: {erro}"
    ok, erro = validar_golos(golos_fora)
    if not ok:
        return 400, f"Golos de fora inválidos: {erro}"

    novo_jogo = {
        "id_jogo": gerar_id_de_lista(jogos, "id_jogo"),
        "data": data,
        "estadio": estadio.strip(),
        "id_clube_casa": id_clube_casa,
        "id_clube_fora": id_clube_fora,
        "golos_casa": int(golos_casa),
        "golos_fora": int(golos_fora),
        "marcadores": [],      # lista de id_jogador que marcaram
        "convocados": [],      # lista de id_jogador convocados
    }
    jogos.append(novo_jogo)
    return 201, novo_jogo


# ============================================================
# LISTAR TODOS
# ============================================================

def listar_jogos():
    """
    Retorna todos os jogos registados.

    Returns:
        tuple: (200, lista) ou (204, mensagem) se vazio
    """
    if not jogos:
        return 204, "Nenhum jogo registado."
    return 200, jogos


# ============================================================
# OBTER UM
# ============================================================

def obter_jogo(id_jogo):
    """
    Procura um jogo pelo seu ID.

    Returns:
        tuple: (200, jogo) ou (404, mensagem)
    """
    for j in jogos:
        if j["id_jogo"] == id_jogo:
            return 200, j
    return 404, "Jogo não encontrado."


# ============================================================
# ATUALIZAR
# ============================================================

def atualizar_jogo(id_jogo, golos_casa=None, golos_fora=None, estadio=None):
    """
    Atualiza campos de um jogo existente, validando cada campo fornecido.

    Returns:
        tuple: (200, jogo atualizado) ou (400/404, mensagem de erro)
    """
    for j in jogos:
        if j["id_jogo"] == id_jogo:

            if golos_casa is not None:
                ok, erro = validar_golos(golos_casa)
                if not ok:
                    return 400, f"Golos da casa inválidos: {erro}"
                j["golos_casa"] = int(golos_casa)

            if golos_fora is not None:
                ok, erro = validar_golos(golos_fora)
                if not ok:
                    return 400, f"Golos de fora inválidos: {erro}"
                j["golos_fora"] = int(golos_fora)

            if estadio is not None:
                ok, erro = validar_nome(estadio)
                if not ok:
                    return 400, f"Estádio inválido: {erro}"
                j["estadio"] = estadio.strip()

            return 200, j

    return 404, "Jogo não encontrado."


# ============================================================
# REMOVER
# ============================================================

def remover_jogo(id_jogo):
    """
    Remove um jogo da lista pelo seu ID.

    Returns:
        tuple: (200, jogo removido) ou (404, mensagem)
    """
    for j in jogos:
        if j["id_jogo"] == id_jogo:
            jogos.remove(j)
            return 200, j
    return 404, "Jogo não encontrado."
