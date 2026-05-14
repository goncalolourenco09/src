import json
import os

# ============================================================
# FICHEIROS DE DADOS
# ============================================================

FICHEIRO_CLUBES      = "clubes.json"
FICHEIRO_JOGADORES   = "jogadores.json"
FICHEIRO_TREINADORES = "treinadores.json"
FICHEIRO_JOGOS       = "jogos.json"


# ============================================================
# FUNÇÕES GENÉRICAS DE PERSISTÊNCIA
# ============================================================

def guardar(ficheiro: str, dados: dict) -> None:
    """Guarda um dicionário num ficheiro JSON."""
    with open(ficheiro, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def carregar(ficheiro: str) -> dict:
    """
    Carrega um dicionário de um ficheiro JSON.
    Devolve {} se o ficheiro não existir.
    """
    if os.path.exists(ficheiro):
        with open(ficheiro, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
