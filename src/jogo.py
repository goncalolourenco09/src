from persistencia import carregar, guardar, FICHEIROS, proximo_id


def validar_estadio(nome: str) -> bool:
    """Valida se o nome do estádio tem pelo menos 3 caracteres."""
    return isinstance(nome, str) and len(nome.strip()) >= 3


def criar_jogo(data: str, estadio: str, id_casa, id_fora, golos_casa=0, golos_fora=0):
    """Cria um novo jogo após validar os dados."""

    # Validar Estádio (substituindo o validar_nome que não existia)
    if not validar_estadio(estadio):
        return False, "Nome do estádio inválido (mínimo 3 caracteres)"

    # Validar se os clubes são diferentes
    if str(id_casa) == str(id_fora):
        return False, "O clube da casa não pode ser o mesmo que o de fora"

    try:
        # Tentar converter golos para inteiro caso venham como string da interface
        g_casa = int(golos_casa)
        g_fora = int(golos_fora)
    except (ValueError, TypeError):
        return False, "Os golos devem ser números inteiros"

    try:
        jogos = carregar(FICHEIROS["jogos"])
        novo_id = str(proximo_id(jogos))

        jogos[novo_id] = {
            "data": data,
            "estadio": estadio.strip(),
            "id_clube_casa": str(id_casa),
            "id_clube_fora": str(id_fora),
            "golos_casa": g_casa,
            "golos_fora": g_fora
        }

        guardar(FICHEIROS["jogos"], jogos)
        return True, novo_id
    except Exception as e:
        return False, f"Erro ao guardar jogo: {str(e)}"


def listar_jogos():
    """Retorna o dicionário de jogos."""
    try:
        return carregar(FICHEIROS["jogadores"])  # Nota: Verifique se o nome no FICHEIROS está correto
    except:
        # Fallback caso a chave no FICHEIROS seja "jogos"
        try:
            from persistencia import FICHEIROS
            return carregar(FICHEIROS.get("jogos", "jogos.json"))
        except:
            return {}


def remover_jogo(id_jogo: str):
    """Remove um jogo pelo ID."""
    try:
        jogos = carregar(FICHEIROS["jogos"])
        id_str = str(id_jogo)
        if id_str not in jogos:
            return False, "Jogo não encontrado"

        del jogos[id_str]
        guardar(FICHEIROS["jogos"], jogos)
        return True, "Jogo removido com sucesso"
    except Exception as e:
        return False, f"Erro ao remover: {str(e)}"

def remover_jogo(id_jogo: str):
    jogos = listar_jogos()
    if id_jogo not in jogos:
        return False, "Jogo não encontrado"
    del jogos[id_jogo]
    guardar(FICHEIROS["jogos"], jogos)
    return True, "Jogo removido"
