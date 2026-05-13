from persistencia import guardar, carregar

# ============================================================
# DADOS EM MEMÓRIA  (carregados do ficheiro ao arrancar)
# ============================================================

clubes = carregar("clubes")


def _proximo_id() -> int:
    """Devolve o próximo ID disponível com base nos dados já existentes."""
    if not clubes:
        return 1
    return max(c["id_clube"] for c in clubes) + 1


# ============================================================
# CRIAR
# ============================================================

def criar_clube(nome, nif):
    """
    Cria um novo clube após validar que o NIF não está duplicado.

    Returns:
        tuple: (201, clube criado) ou (409, mensagem de erro)
    """
    # Verificar NIF duplicado
    for c in clubes:
        if c["nif"] == nif:
            return 409, "Conflito: clube com este NIF já existe."

    clube = {
        "id_clube": _proximo_id(),
        "nome": nome.strip(),
        "nif": nif,
    }
    clubes.append(clube)
    guardar("clubes", clubes)          # ← persistência
    return 201, clube


# ============================================================
# LISTAR TODOS
# ============================================================

def listar_clubes():
    """
    Retorna todos os clubes registados.

    Returns:
        tuple: (200, lista) ou (204, mensagem) se vazio
    """
    if not clubes:
        return 204, "Nenhum clube registado."
    return 200, clubes


# ============================================================
# OBTER UM
# ============================================================

def obter_clube(id_clube):
    """
    Procura um clube pelo seu ID.

    Returns:
        tuple: (200, clube) ou (404, mensagem)
    """
    for c in clubes:
        if c["id_clube"] == id_clube:
            return 200, c
    return 404, "Clube não encontrado."


# ============================================================
# ATUALIZAR
# ============================================================

def atualizar_clube(id_clube, nome=None, nif=None):
    """
    Atualiza campos de um clube existente.

    Returns:
        tuple: (200, clube atualizado) ou (400/404/409, mensagem de erro)
    """
    for c in clubes:
        if c["id_clube"] == id_clube:

            if nome is not None:
                c["nome"] = nome.strip()

            if nif is not None:
                # Verificar NIF duplicado (excluindo o próprio clube)
                for outro in clubes:
                    if outro["nif"] == nif and outro["id_clube"] != id_clube:
                        return 409, "Conflito: NIF já pertence a outro clube."
                c["nif"] = nif

            guardar("clubes", clubes)  # ← persistência
            return 200, c

    return 404, "Clube não encontrado."


# ============================================================
# REMOVER
# ============================================================

def remover_clube(id_clube):
    """
    Remove um clube da lista pelo seu ID.

    Returns:
        tuple: (200, clube removido) ou (404, mensagem)
    """
    for c in clubes:
        if c["id_clube"] == id_clube:
            clubes.remove(c)
            guardar("clubes", clubes)  # ← persistência
            return 200, c
    return 404, "Clube não encontrado."
