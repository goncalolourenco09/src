from persistencia import carregar, guardar, FICHEIROS, proximo_id
from datetime import datetime, date

def validar_posicao(posicao: str) -> bool:
    posicoes = ["guarda-redes", "defesa", "médio", "avançado"]
    return posicao.lower() in posicoes

def criar_jogador(nome: str, data_nasc: str, numero_camisa: int, posicao: str, salario: float):
    if not validar_nome(nome):
        return False, "Nome inválido"
    if not validar_posicao(posicao):
        return False, "Posição inválida"
    if not isinstance(numero_camisa, int) or numero_camisa < 1 or numero_camisa > 99:
        return False, "Número de camisola inválido (1-99)"

    try:
        datetime.strptime(data_nasc, "%Y-%m-%d")
    except:
        return False, "Data inválida (use YYYY-MM-DD)"

    idade = date.today().year - datetime.strptime(data_nasc, "%Y-%m-%d").year

    jogadores = carregar(FICHEIROS["jogadores"])
    novo_id = str(proximo_id(jogadores))

    jogadores[novo_id] = {
        "nome": nome.strip(),
        "data_nascimento": data_nasc,
        "idade": idade,
        "posicao": posicao,
        "numero_camisa": numero_camisa,
        "salario": float(salario)
    }
    guardar(FICHEIROS["jogadores"], jogadores)
    return True, novo_id

def listar_jogadores():
    return carregar(FICHEIROS["jogadores"])

def remover_jogador(id_jogador: str):
    jogadores = listar_jogadores()
    if id_jogador not in jogadores:
        return False, "Jogador não encontrado"
    del jogadores[id_jogador]
    guardar(FICHEIROS["jogadores"], jogadores)
    return True, "Jogador removido"
