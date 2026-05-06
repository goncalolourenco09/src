from utils import (
    gerar_id_de_lista,
    validar_nome,
    validar_data,
    validar_salario,
    validar_numero_camisola,
    validar_posicao,
    calcular_idade,
)

# ============================================================
# DADOS EM MEMÓRIA
# ============================================================

jogadores = []

# Dicionário auxiliar: número de camisola → id_jogador
jogador_por_camisola = {}


# ============================================================
# UTILITÁRIOS INTERNOS
# ============================================================

def _atualizar_dicionario_camisolas():
    """Reconstrói o índice camisola→jogador a partir da lista atual."""
    jogador_por_camisola.clear()
    for j in jogadores:
        jogador_por_camisola[j["numero_camisa"]] = j["id_jogador"]


def _camisola_em_uso(numero, excluir_id=None):
    """
    Verifica se um número de camisola já está em uso.
    excluir_id permite ignorar o próprio jogador em atualizações.
    """
    for j in jogadores:
        if j["numero_camisa"] == numero and j["id_jogador"] != excluir_id:
            return True
    return False


# ============================================================
# CRIAR
# ============================================================

def criar_jogador(nome, data_nascimento, numero_camisa, posicao, salario):
    """
    Cria um novo jogador após validar todos os campos.

    Returns:
        tuple: (código HTTP, jogador criado ou mensagem de erro)
    """
    # Validar nome
    ok, erro = validar_nome(nome)
    if not ok:
        return 400, erro

    # Validar data de nascimento
    ok, erro = validar_data(data_nascimento)
    if not ok:
        return 400, erro

    # Validar número de camisola
    ok, erro = validar_numero_camisola(numero_camisa)
    if not ok:
        return 400, erro

    # Verificar camisola duplicada
    if _camisola_em_uso(int(numero_camisa)):
        return 409, f"Conflito: camisola {numero_camisa} já está em uso."

    # Validar posição
    ok, erro = validar_posicao(posicao)
    if not ok:
        return 400, erro

    # Validar salário
    ok, erro = validar_salario(salario)
    if not ok:
        return 400, erro

    jogador = {
        "id_jogador": gerar_id_de_lista(jogadores, "id_jogador"),
        "nome": nome.strip(),
        "data_nascimento": data_nascimento,
        "idade": calcular_idade(data_nascimento),
        "posicao": posicao.strip().title(),
        "numero_camisa": int(numero_camisa),
        "salario": float(salario),
    }
    jogadores.append(jogador)
    _atualizar_dicionario_camisolas()
    return 201, jogador


# ============================================================
# LISTAR TODOS
# ============================================================

def listar_jogadores():
    """
    Retorna todos os jogadores registados.

    Returns:
        tuple: (200, lista) ou (204, mensagem) se vazio
    """
    if not jogadores:
        return 204, "Sem jogadores registados."
    return 200, jogadores


# ============================================================
# OBTER UM
# ============================================================

def obter_jogador(id_jogador):
    """
    Procura um jogador pelo seu ID.

    Returns:
        tuple: (200, jogador) ou (404, mensagem)
    """
    for j in jogadores:
        if j["id_jogador"] == id_jogador:
            return 200, j
    return 404, "Jogador não encontrado."


# ============================================================
# ATUALIZAR
# ============================================================

def atualizar_jogador(id_jogador, nome=None, numero_camisa=None, salario=None, posicao=None):
    """
    Atualiza campos de um jogador existente, validando cada campo fornecido.

    Returns:
        tuple: (200, jogador atualizado) ou (400/404, mensagem de erro)
    """
    for j in jogadores:
        if j["id_jogador"] == id_jogador:

            if nome is not None:
                ok, erro = validar_nome(nome)
                if not ok:
                    return 400, erro
                j["nome"] = nome.strip()

            if numero_camisa is not None:
                ok, erro = validar_numero_camisola(numero_camisa)
                if not ok:
                    return 400, erro
                if _camisola_em_uso(int(numero_camisa), excluir_id=id_jogador):
                    return 409, f"Conflito: camisola {numero_camisa} já está em uso."
                j["numero_camisa"] = int(numero_camisa)

            if salario is not None:
                ok, erro = validar_salario(salario)
                if not ok:
                    return 400, erro
                j["salario"] = float(salario)

            if posicao is not None:
                ok, erro = validar_posicao(posicao)
                if not ok:
                    return 400, erro
                j["posicao"] = posicao.strip().title()

            _atualizar_dicionario_camisolas()
            return 200, j

    return 404, "Jogador não encontrado."


# ============================================================
# REMOVER
# ============================================================

def remover_jogador(id_jogador):
    """
    Remove um jogador da lista pelo seu ID.

    Returns:
        tuple: (200, jogador removido) ou (404, mensagem)
    """
    for j in jogadores:
        if j["id_jogador"] == id_jogador:
            jogadores.remove(j)
            _atualizar_dicionario_camisolas()
            return 200, j
    return 404, "Jogador não encontrado."
