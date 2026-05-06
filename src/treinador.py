from utils import (
    gerar_id_de_lista,
    validar_nome,
    validar_data,
    validar_licenca_UEFA,
)

# ============================================================
# DADOS EM MEMÓRIA
# ============================================================

treinadores = []


# ============================================================
# CRIAR
# ============================================================

def criar_treinador(nome, nacionalidade, data_nascimento, licenca_UEFA, id_clube=None):
    """
    Cria um novo treinador após validar todos os campos.

    Returns:
        tuple: (201, treinador criado) ou (400, mensagem de erro)
    """
    # Validar nome
    ok, erro = validar_nome(nome)
    if not ok:
        return 400, erro

    # Validar nacionalidade
    ok, erro = validar_nome(nacionalidade)
    if not ok:
        return 400, f"Nacionalidade inválida: {erro}"

    # Validar data de nascimento
    ok, erro = validar_data(data_nascimento)
    if not ok:
        return 400, erro

    # Validar licença UEFA
    ok, erro = validar_licenca_UEFA(licenca_UEFA)
    if not ok:
        return 400, erro

    # Validar id_clube (opcional, mas se fornecido deve ser inteiro positivo)
    if id_clube is not None:
        if not isinstance(id_clube, int) or id_clube <= 0:
            return 400, "ID de clube inválido: deve ser um inteiro positivo."

    novo_treinador = {
        "id_treinador": gerar_id_de_lista(treinadores, "id_treinador"),
        "nome": nome.strip(),
        "nacionalidade": nacionalidade.strip(),
        "data_nascimento": data_nascimento,
        "licenca_UEFA": licenca_UEFA.strip().upper(),
        "id_clube": id_clube,
    }
    treinadores.append(novo_treinador)
    return 201, novo_treinador


# ============================================================
# LISTAR TODOS
# ============================================================

def listar_treinadores():
    """
    Retorna todos os treinadores registados.

    Returns:
        tuple: (200, lista) ou (204, mensagem) se vazio
    """
    if not treinadores:
        return 204, "Nenhum treinador registado."
    return 200, treinadores


# ============================================================
# OBTER UM
# ============================================================

def obter_treinador(id_treinador):
    """
    Procura um treinador pelo seu ID.

    Returns:
        tuple: (200, treinador) ou (404, mensagem)
    """
    for t in treinadores:
        if t["id_treinador"] == id_treinador:
            return 200, t
    return 404, "Treinador não encontrado."


# ============================================================
# ATUALIZAR
# ============================================================

def atualizar_treinador(id_treinador, nome=None, nacionalidade=None, licenca_UEFA=None, id_clube=None):
    """
    Atualiza campos de um treinador existente, validando cada campo fornecido.

    Returns:
        tuple: (200, treinador atualizado) ou (400/404, mensagem de erro)
    """
    for t in treinadores:
        if t["id_treinador"] == id_treinador:

            if nome is not None:
                ok, erro = validar_nome(nome)
                if not ok:
                    return 400, erro
                t["nome"] = nome.strip()

            if nacionalidade is not None:
                ok, erro = validar_nome(nacionalidade)
                if not ok:
                    return 400, f"Nacionalidade inválida: {erro}"
                t["nacionalidade"] = nacionalidade.strip()

            if licenca_UEFA is not None:
                ok, erro = validar_licenca_UEFA(licenca_UEFA)
                if not ok:
                    return 400, erro
                t["licenca_UEFA"] = licenca_UEFA.strip().upper()

            if id_clube is not None:
                if not isinstance(id_clube, int) or id_clube <= 0:
                    return 400, "ID de clube inválido: deve ser um inteiro positivo."
                t["id_clube"] = id_clube

            return 200, t

    return 404, "Treinador não encontrado."


# ============================================================
# REMOVER
# ============================================================

def remover_treinador(id_treinador):
    """
    Remove um treinador da lista pelo seu ID.

    Returns:
        tuple: (200, treinador removido) ou (404, mensagem)
    """
    for t in treinadores:
        if t["id_treinador"] == id_treinador:
            treinadores.remove(t)
            return 200, t
    return 404, "Treinador não encontrado."
