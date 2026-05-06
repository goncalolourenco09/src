from datetime import datetime
 
# ============================================================
# GERAÇÃO DE IDs
# ============================================================
 
def gerar_id_de_lista(lista, campo_id):
    """
    Gera um novo ID único baseado no maior ID existente na lista.
    Garante que nunca há colisão, mesmo após remoções.
 
    Args:
        lista (list): lista de dicionários com os registos
        campo_id (str): nome da chave de ID (ex: "id_jogador")
 
    Returns:
        int: novo ID único
    """
    if not lista:
        return 1
    return max(item[campo_id] for item in lista) + 1
 
 
# ============================================================
# VALIDAÇÕES DE DATA
# ============================================================
 
def validar_data(data_str, formato="%Y-%m-%d"):
    """
    Verifica se uma string de data é válida e não está no futuro.
 
    Args:
        data_str (str): data em formato string (ex: "2000-05-21")
        formato (str): formato esperado (padrão: "%Y-%m-%d")
 
    Returns:
        tuple: (True, datetime) se válida | (False, mensagem de erro)
    """
    if not data_str or not isinstance(data_str, str):
        return False, "Data inválida: valor vazio ou não é uma string."
    try:
        data = datetime.strptime(data_str, formato)
    except ValueError:
        return False, f"Data inválida: formato esperado {formato} (ex: '2000-05-21')."
 
    if data > datetime.now():
        return False, "Data inválida: a data não pode ser no futuro."
 
    return True, data
 
 
def validar_intervalo_datas(data_inicio_str, data_fim_str, formato="%Y-%m-%d"):
    """
    Verifica se duas datas formam um intervalo válido (início <= fim).
 
    Args:
        data_inicio_str (str): data de início
        data_fim_str (str): data de fim
        formato (str): formato esperado
 
    Returns:
        tuple: (True, None) se válido | (False, mensagem de erro)
    """
    try:
        inicio = datetime.strptime(data_inicio_str, formato)
        fim = datetime.strptime(data_fim_str, formato)
    except ValueError:
        return False, f"Datas inválidas: formato esperado {formato}."
 
    if inicio > fim:
        return False, "Data de início não pode ser posterior à data de fim."
 
    return True, None
 
 
def calcular_idade(data_nascimento_str, formato="%Y-%m-%d"):
    """
    Calcula a idade em anos a partir de uma data de nascimento.
 
    Args:
        data_nascimento_str (str): data de nascimento
        formato (str): formato esperado
 
    Returns:
        int | None: idade em anos, ou None se a data for inválida
    """
    valida, resultado = validar_data(data_nascimento_str, formato)
    if not valida:
        return None
    hoje = datetime.now()
    nascimento = resultado
    idade = hoje.year - nascimento.year
    # Ajuste se ainda não fez aniversário este ano
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1
    return idade
 
 
# ============================================================
# VALIDAÇÕES DE CAMPOS COMUNS
# ============================================================
 
def validar_nome(nome):
    """
    Valida que o nome não está vazio e tem pelo menos 2 caracteres.
 
    Returns:
        tuple: (True, None) se válido | (False, mensagem de erro)
    """
    if not nome or not isinstance(nome, str) or len(nome.strip()) < 2:
        return False, "Nome inválido: deve ter pelo menos 2 caracteres."
    return True, None
 
 
def validar_salario(salario):
    """
    Valida que o salário é um número positivo.
 
    Returns:
        tuple: (True, None) se válido | (False, mensagem de erro)
    """
    try:
        valor = float(salario)
    except (TypeError, ValueError):
        return False, "Salário inválido: deve ser um número."
    if valor < 0:
        return False, "Salário inválido: não pode ser negativo."
    return True, None
 
 
def validar_numero_camisola(numero):
    """
    Valida que o número de camisola é inteiro e está entre 1 e 99.
 
    Returns:
        tuple: (True, None) se válido | (False, mensagem de erro)
    """
    try:
        n = int(numero)
    except (TypeError, ValueError):
        return False, "Número de camisola inválido: deve ser um número inteiro."
    if not (1 <= n <= 99):
        return False, "Número de camisola inválido: deve estar entre 1 e 99."
    return True, None
 
 
def validar_golos(golos):
    """
    Valida que os golos são um número inteiro não negativo.
 
    Returns:
        tuple: (True, None) se válido | (False, mensagem de erro)
    """
    try:
        g = int(golos)
    except (TypeError, ValueError):
        return False, "Golos inválidos: deve ser um número inteiro."
    if g < 0:
        return False, "Golos inválidos: não pode ser negativo."
    return True, None
 
 
def validar_licenca_UEFA(licenca):
    """
    Valida que a licença UEFA é uma das categorias reconhecidas.
 
    Returns:
        tuple: (True, None) se válido | (False, mensagem de erro)
    """
    licencas_validas = {"A", "B", "PRO", "UEFA PRO", "UEFA A", "UEFA B"}
    if not licenca or licenca.strip().upper() not in licencas_validas:
        return False, f"Licença UEFA inválida. Valores aceites: {licencas_validas}"
    return True, None
 
 
def validar_posicao(posicao):
    """
    Valida que a posição é uma das aceites.
 
    Returns:
        tuple: (True, None) se válido | (False, mensagem de erro)
    """
    posicoes_validas = {"Guarda-Redes", "Defesa", "Médio", "Avançado"}
    if not posicao or posicao.strip().title() not in posicoes_validas:
        return False, f"Posição inválida. Valores aceites: {posicoes_validas}"
    return True, None
