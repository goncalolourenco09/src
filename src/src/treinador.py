from database import SessionLocal
from models import Treinador


def criar_treinador(nome, nacionalidade, data_nascimento, licenca_UEFA, id_clube=None):
    db = SessionLocal()
    try:
        treinador = Treinador(
            nome=nome,
            nacionalidade=nacionalidade,
            data_nascimento=data_nascimento,
            licenca_UEFA=licenca_UEFA,
            id_clube=id_clube,
        )
        db.add(treinador)
        db.commit()
        db.refresh(treinador)
        return 201, {"id_treinador": treinador.id_treinador, "nome": treinador.nome}
    except Exception as e:
        db.rollback()
        return 500, str(e)
    finally:
        db.close()


def listar_treinadores():
    db = SessionLocal()
    try:
        treinadores = db.query(Treinador).all()
        if not treinadores:
            return 200, "Nenhum treinador encontrado."
        return 200, [
            {
                "id_treinador": t.id_treinador,
                "nome": t.nome,
                "nacionalidade": t.nacionalidade,
                "data_nascimento": str(t.data_nascimento),
                "licenca_UEFA": t.licenca_UEFA,
                "id_clube": t.id_clube,
            }
            for t in treinadores
        ]
    except Exception as e:
        return 500, str(e)
    finally:
        db.close()


def obter_treinador(id_treinador):
    db = SessionLocal()
    try:
        treinador = db.query(Treinador).filter(Treinador.id_treinador == id_treinador).first()
        if not treinador:
            return 404, "Treinador não encontrado."
        return 200, {
            "id_treinador": treinador.id_treinador,
            "nome": treinador.nome,
            "nacionalidade": treinador.nacionalidade,
            "data_nascimento": str(treinador.data_nascimento),
            "licenca_UEFA": treinador.licenca_UEFA,
            "id_clube": treinador.id_clube,
        }
    except Exception as e:
        return 500, str(e)
    finally:
        db.close()


def atualizar_treinador(id_treinador, nome=None, nacionalidade=None, licenca_UEFA=None, id_clube=None):
    db = SessionLocal()
    try:
        treinador = db.query(Treinador).filter(Treinador.id_treinador == id_treinador).first()
        if not treinador:
            return 404, "Treinador não encontrado."
        if nome:
            treinador.nome = nome
        if nacionalidade:
            treinador.nacionalidade = nacionalidade
        if licenca_UEFA:
            treinador.licenca_UEFA = licenca_UEFA
        if id_clube is not None:
            treinador.id_clube = id_clube
        db.commit()
        return 200, "Treinador atualizado com sucesso."
    except Exception as e:
        db.rollback()
        return 500, str(e)
    finally:
        db.close()


def remover_treinador(id_treinador):
    db = SessionLocal()
    try:
        treinador = db.query(Treinador).filter(Treinador.id_treinador == id_treinador).first()
        if not treinador:
            return 404, "Treinador não encontrado."
        nome = treinador.nome
        db.delete(treinador)
        db.commit()
        return 200, {"nome": nome}
    except Exception as e:
        db.rollback()
        return 500, str(e)
    finally:
        db.close()