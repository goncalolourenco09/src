from persistencia import carregar, guardar, FICHEIROS, proximo_id
from datetime import datetime, date


def validar_nome(nome: str) -> bool:
    return isinstance(nome, str) and len(nome.strip()) >= 3


def validar_posicao(posicao: str) -> bool:
    posicoes = ["guarda-redes", "defesa", "médio", "avançado"]
    return str(posicao).lower() in posicoes


def criar_jogador(nome: str, data_nasc: str, numero_camisa, posicao: str, salario):
    # Validar Nome
    if not validar_nome(nome):
        return False, "Nome inválido (mínimo 3 caracteres)"

    # Validar Posição
    if not validar_posicao(posicao):
        return False, "Posição inválida"

    # Validar e Converter Número Camisola
    try:
        num = int(numero_camisa)
        if num < 1 or num > 99:
            return False, "Número de camisola deve estar entre 1 e 99"
    except (ValueError, TypeError):
        return False, "Número de camisola deve ser um número inteiro"

    # Validar e Converter Salário
    try:
        sal = float(salario)
        if sal < 0:
            return False, "Salário não pode ser negativo"
    except (ValueError, TypeError):
        return False, "Salário deve ser um valor numérico"

    # Validar Data e Calcular Idade
    try:
        data_dt = datetime.strptime(data_nasc, "%Y-%m-%d")
        hoje = date.today()
        idade = hoje.year - data_dt.year - ((hoje.month, hoje.day) < (data_dt.month, data_dt.day))
    except ValueError:
        return False, "Data inválida! Use o formato AAAA-MM-DD"

    try:
        jogadores = carregar(FICHEIROS["jogadores"])
        novo_id = str(proximo_id(jogadores))

        jogadores[novo_id] = {
            "nome": nome.strip(),
            "data_nascimento": data_nasc,
            "idade": idade,
            "posicao": posicao.lower(),
            "numero_camisa": num,
            "salario": sal
        }

        guardar(FICHEIROS["jogadores"], jogadores)
        return True, novo_id
    except Exception as e:
        return False, f"Erro na base de dados: {str(e)}"


def listar_jogadores():
    try:
        return carregar(FICHEIROS["jogadores"])
    except:
        return {}


def remover_jogador(id_jogador: str):
    try:
        jogadores = listar_jogadores()
        if str(id_jogador) not in jogadores:
            return False, "Jogador não encontrado"
        del jogadores[str(id_jogador)]
        guardar(FICHEIROS["jogadores"], jogadores)
        return True, "Jogador removido"
    except Exception as e:
        return False, f"Erro ao remover: {str(e)}"
