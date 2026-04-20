from datetime import datetime


def atualizar_dic():
    jogador_por_camisola.clear()
    for j in jogadores:
        jogador_por_camisola[j["numero_camisa"]] = j["id_jogador"]

def gerar_id():
    return max([j["id_jogador"] for j in jogadores], default=0) + 1



def calcular_idade(data_nascimento):
    hoje = datetime.now()
    nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    return hoje.year - nascimento.year