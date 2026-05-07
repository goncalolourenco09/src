from datetime import datetime, date


# ============================================================
# GERAR ID
# ============================================================

def gerar_id_de_lista(lista, campo_id):
    if not lista:
        return 1
    return max(item[campo_id] for item in lista) + 1


# ============================================================
# VALIDAÇÕES
# ============================================================

def validar_nome(nome):
    if nome == "" or nome == None:
        return False, "Nome não pode estar vazio."
    if len(nome) < 2:
        return False, "Nome deve ter pelo menos 2 caracteres."
    return True, None


def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True, None
    except ValueError:
        return False, "Data inválida. Use o formato YYYY-MM-DD."


def validar_salario(salario):
    if salario < 0:
        return False, "Salário não pode ser negativo."
    return True, None


def validar_numero_camisola(numero):
    if numero < 1 or numero > 99:
        return False, "Número de camisola deve estar entre 1 e 99."
    return True, None


def validar_posicao(posicao):
    posicoes_validas = ["guarda-redes", "defesa", "médio", "avançado"]
    if posicao.lower() not in posicoes_validas:
        return False, "Posição inválida. Escolha entre: guarda-redes, defesa, médio, avançado."
    return True, None


def validar_licenca_UEFA(licenca):
    licencas_validas = ["A", "B", "PRO"]
    if licenca.upper() not in licencas_validas:
        return False, "Licença UEFA inválida. Escolha entre: A, B, Pro."
    return True, None


def validar_golos(golos):
    if golos < 0:
        return False, "Golos não podem ser negativos."
    return True, None


def calcular_idade(data_nascimento_str):
    nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
    hoje = date.today()
    idade = hoje.year - nascimento.year
    return idade
