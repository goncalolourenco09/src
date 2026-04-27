from database import SessionLocal
from models import Jogo


def criar_jogo(data, estadio, id_clube_casa, id_clube_fora, golos_casa=0, golos_fora=0):
    db = SessionLocal()
    try:
        jogo = Jogo(
            data=data,
            estadio=estadio,
            id_clube_casa=id_clube_casa,
            id_clube_fora=id_clube_fora,
            golos_casa=golos_casa,
            golos_fora=golos_fora,
        )
        db.add(jogo)
        db.commit()
        db.refresh(jogo)
        return 201, {"id_jogo": jogo.id_jogo, "estadio": jogo.estadio}
    except Exception as e:
        db.rollback()
        return 500, str(e)
    finally:
        db.close()


def listar_jogos():
    db = SessionLocal()
    try:
        jogos = db.query(Jogo).all()
        if not jogos:
            return 200, "Nenhum jogo encontrado."
        return 200, [
            {
                "id_jogo": j.id_jogo,
                "data": str(j.data),
                "estadio": j.estadio,
                "id_clube_casa": j.id_clube_casa,
                "id_clube_fora": j.id_clube_fora,
                "golos_casa": j.golos_casa,
                "golos_fora": j.golos_fora,
            }
            for j in jogos
        ]
    except Exception as e:
        return 500, str(e)
    finally:
        db.close()


def obter_jogo(id_jogo):
    db = SessionLocal()
    try:
        jogo = db.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
        if not jogo:
            return 404, "Jogo não encontrado."
        return 200, {
            "id_jogo": jogo.id_jogo,
            "data": str(jogo.data),
            "estadio": jogo.estadio,
            "id_clube_casa": jogo.id_clube_casa,
            "id_clube_fora": jogo.id_clube_fora,
            "golos_casa": jogo.golos_casa,
            "golos_fora": jogo.golos_fora,
        }
    except Exception as e:
        return 500, str(e)
    finally:
        db.close()


def atualizar_jogo(id_jogo, golos_casa=None, golos_fora=None, estadio=None):
    db = SessionLocal()
    try:
        jogo = db.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
        if not jogo:
            return 404, "Jogo não encontrado."
        if golos_casa is not None:
            jogo.golos_casa = golos_casa
        if golos_fora is not None:
            jogo.golos_fora = golos_fora
        if estadio:
            jogo.estadio = estadio
        db.commit()
        return 200, "Jogo atualizado com sucesso."
    except Exception as e:
        db.rollback()
        return 500, str(e)
    finally:
        db.close()


def remover_jogo(id_jogo):
    db = SessionLocal()
    try:
        jogo = db.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
        if not jogo:
            return 404, "Jogo não encontrado."
        db.delete(jogo)
        db.commit()
        return 200, {"id_jogo": id_jogo}
    except Exception as e:
        db.rollback()
        return 500, str(e)
    finally:
        db.close()