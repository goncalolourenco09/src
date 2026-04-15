clubes = []
ultimo_id_clube = 0


def gerar_id_clube():
    global ultimo_id_clube
    ultimo_id_clube += 1
    return ultimo_id_clube


def criar_clube(nome, nif):
    # verificar se já existe NIF
    for c in clubes:
        if c["nif"] == nif:
            return 409, "Clube com este NIF já existe!"

    clube = {
        "id_clube": gerar_id_clube(),
        "nome": nome,
        "nif": nif
    }

    clubes.append(clube)
    return 200, clube


def remover_clube(id_clube):
    for c in clubes:
        if c["id_clube"] == id_clube:
            clubes.remove(c)
            return 200, c

    return 404, "Clube não encontrado"

def listar_clube():
    if len(clube)0:
        return 204, "sem clubes registados"
    return 200, clubes
