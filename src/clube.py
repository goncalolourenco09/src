def criar_clube_service(nome, nif):
    clube = {
        "id_clube": len(clubes) + 1,
        "nome": nome,
        "nif": nif,
        "jogadores": []
    }

    clubes.append(clube)
    return (200, clube)

def remover_clube_service(id_clube):
        for c in clubes:
            if c["id_clube"] == id_clube:
                clubes.remove(c)
                return (200, c)

        return (404, "Clube não encontrado")