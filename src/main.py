import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

from treinador import (
    criar_treinador,
    atualizar_treinador,
    listar_treinadores,
    remover_treinador,
    consultar_treinador,
)
from jogo import (
    remover_jogo,
    consultar_jogo,
    atualizar_jogo,
    listar_jogos,
    criar_jogo,
)
from clube import (
    remover_clube,
    criar_clube,
    listar_clubes,
)
from jogador import (
    criar_jogador,
    listar_jogadores,
    remover_jogador,
    consultar_jogador,
    atualizar_jogador,
)


def main():
    logger.info("Sistema iniciado")
    while True:
        print("""
            1. Adicionar jogador
            2. Listar jogadores
            3. Procurar jogador
            4. Atualizar jogador
            5. Remover jogador
            6. Adicionar clube
            7. Remover clube
            8. Listar clubes
            9. Adicionar treinador
            10. Listar treinadores
            11. Procurar treinador
            12. Atualizar treinador
            13. Remover treinador
            14. Adicionar jogo
            15. Listar jogos
            16. Procurar jogo
            17. Atualizar jogo
            18. Remover jogo
            0. Sair
        """)
        op = input("Opção: ")

        if op == "1":
            nome = input("Nome: ")

            from datetime import datetime
            while True:
                data_nascimento = input("Data nascimento (YYYY-MM-DD): ")
                try:
                    datetime.strptime(data_nascimento, "%Y-%m-%d")
                    break
                except ValueError:
                    print(" Data inválida! Use o formato YYYY-MM-DD (ex: 2000-05-23)")

            try:
                numero = int(input("Número da camisola: "))
            except ValueError:
                print(" Número da camisola inválido!")
                continue

            posicao = input("Posição: ")

            try:
                salario = float(input("Salário: "))
            except ValueError:
                print(" Salário inválido!")
                continue

            status, dados = criar_jogador(nome, data_nascimento, numero, posicao, salario)

            if status == 201:
                print(f" Jogador {dados['nome']} adicionado!")
            else:
                logger.error("Erro ao adicionar jogador via menu — código %s: %s", status, dados)
                print(f" ERRO - {status}: {dados}")

        elif op == "2":
            status, dados = listar_jogadores()

            if status in (200, 204):
                if isinstance(dados, str):
                    print(dados)
                else:
                    print("\n--- Jogadores ---")
                    for j in dados:
                        print(f'{j["id_jogador"]} | {j["nome"]} | Nº {j["numero_camisa"]}')
            else:
                logger.error("Erro ao listar jogadores — código %s: %s", status, dados)
                print("", dados)

        elif op == "3":
            try:
                id_jogador = int(input("ID do jogador: "))
                status, jogador = obter_jogador(id_jogador)

                if status == 200:
                    print("\n--- Detalhes do Jogador ---")
                    for k, v in jogador.items():
                        print(f"{k}: {v}")
                else:
                    logger.error("Erro ao procurar jogador ID %s — código %s: %s", id_jogador, status, jogador)
                    print("", jogador)
            except ValueError:
                print(" ID inválido!")

        elif op == "4":
            try:
                id_jogador = int(input("ID do jogador: "))
            except ValueError:
                print(" ID inválido!")
                continue

            nome = input("Novo nome (ENTER para manter): ")
            numero = input("Novo número (ENTER para manter): ")

            if numero:
                try:
                    numero = int(numero)
                except ValueError:
                    print(" Número inválido!")
                    continue
            else:
                numero = None

            status, msg = atualizar_jogador(
                id_jogador,
                nome=nome or None,
                numero_camisa=numero,
            )

            if status == 200:
                print(" Jogador atualizado!")
            else:
                logger.error("Erro ao atualizar jogador ID %s — código %s: %s", id_jogador, status, msg)
                print("", msg)

        elif op == "5":
            try:
                id_jogador = int(input("ID: "))
                status, dados = remover_jogador(id_jogador)

                if status == 200:
                    print(" Jogador removido:", dados["nome"])
                else:
                    logger.error("Erro ao remover jogador ID %s — código %s: %s", id_jogador, status, dados)
                    print("", dados)
            except ValueError:
                print(" ID inválido!")

        elif op == "6":
            nome = input("Nome do clube: ")
            nif = input("NIF: ")

            status, dados = criar_clube(nome, nif)

            if status in (200, 201):
                print(" Clube criado:", dados["nome"])
            else:
                logger.error("Erro ao criar clube via menu — código %s: %s", status, dados)
                print("", dados)

        elif op == "7":
            try:
                id_clube = int(input("ID do clube: "))
                status, dados = remover_clube(id_clube)

                if status == 200:
                    print(" Clube removido:", dados["nome"])
                else:
                    logger.error("Erro ao remover clube ID %s — código %s: %s", id_clube, status, dados)
                    print("", dados)
            except ValueError:
                print(" ID inválido!")

        elif op == "8":
            status, dados = listar_clubes()

            if status == 200:
                if isinstance(dados, str):
                    print(dados)
                else:
                    print("\n--- Clubes ---")
                    for c in dados:
                        print(f'{c["id_clube"]} | {c["nome"]} | NIF: {c["nif"]}')
            else:
                logger.error("Erro ao listar clubes — código %s: %s", status, dados)
                print("", dados)

        elif op == "9":
            nome = input("Nome: ")
            nacionalidade = input("Nacionalidade: ")

            from datetime import datetime
            while True:
                data_nascimento = input("Data nascimento (YYYY-MM-DD): ")
                try:
                    datetime.strptime(data_nascimento, "%Y-%m-%d")
                    break
                except ValueError:
                    print(" Data inválida! Use o formato YYYY-MM-DD")

            licenca_UEFA = input("Licença UEFA (A / B / Pro): ")

            try:
                code, clubes = listar_clubes()
                if code == 200:
                    print(clubes)
                    id_clube = int(input("ID do clube (ENTER para nenhum): ") or 0) or None
                else:
                    id_clube = None
            except ValueError:
                id_clube = None

            status, dados = criar_treinador(nome, nacionalidade, data_nascimento, licenca_UEFA, id_clube)

            if status == 201:
                print(f" Treinador {dados['nome']} adicionado!")
            else:
                logger.error("Erro ao adicionar treinador via menu — código %s: %s", status, dados)
                print(f" ERRO - {status}: {dados}")

        elif op == "10":
            status, dados = listar_treinadores()

            if status in (200, 204):
                if isinstance(dados, str):
                    print(dados)
                else:
                    print("\n--- Treinadores ---")
                    for t in dados:
                        print(f'{t["id_treinador"]} | {t["nome"]} | {t["nacionalidade"]} | Licença: {t["licenca_UEFA"]} | Clube: {t["id_clube"]}')
            else:
                logger.error("Erro ao listar treinadores — código %s: %s", status, dados)
                print("", dados)

        elif op == "11":
            try:
                id_treinador = int(input("ID do treinador: "))
                status, treinador = consultar_treinador(id_treinador)

                if status == 200:
                    print("\n--- Detalhes do Treinador ---")
                    for k, v in treinador.items():
                        print(f"{k}: {v}")
                else:
                    logger.error("Erro ao procurar treinador ID %s — código %s: %s", id_treinador, status, treinador)
                    print("", treinador)
            except ValueError:
                print(" ID inválido!")

        elif op == "12":
            try:
                id_treinador = int(input("ID do treinador: "))
            except ValueError:
                print(" ID inválido!")
                continue

            nome = input("Novo nome (ENTER para manter): ")
            nacionalidade = input("Nova nacionalidade (ENTER para manter): ")
            licenca_UEFA = input("Nova licença UEFA (ENTER para manter): ")
            id_clube = input("Novo ID clube (ENTER para manter): ")

            id_clube = int(id_clube) if id_clube else None

            status, msg = atualizar_treinador(
                id_treinador,
                nome or None,
                nacionalidade or None,
                licenca_UEFA or None,
                id_clube,
            )

            if status == 200:
                print(" Treinador atualizado!")
            else:
                logger.error("Erro ao atualizar treinador ID %s — código %s: %s", id_treinador, status, msg)
                print("", msg)

        elif op == "13":
            try:
                id_treinador = int(input("ID do treinador: "))
                status, dados = remover_treinador(id_treinador)

                if status == 200:
                    print(" Treinador removido:", dados["nome"])
                else:
                    logger.error("Erro ao remover treinador ID %s — código %s: %s", id_treinador, status, dados)
                    print("", dados)
            except ValueError:
                print(" ID inválido!")

        elif op == "14":
            from datetime import datetime
            while True:
                data = input("Data do jogo (YYYY-MM-DD): ")
                try:
                    datetime.strptime(data, "%Y-%m-%d")
                    break
                except ValueError:
                    print(" Data inválida! Use o formato YYYY-MM-DD")

            estadio = input("Estádio: ")

            try:
                id_clube_casa = int(input("ID do clube da casa: "))
                id_clube_fora = int(input("ID do clube de fora: "))
                golos_casa = int(input("Golos casa: "))
                golos_fora = int(input("Golos fora: "))
            except ValueError:
                print(" Valor inválido!")
                continue

            status, dados = criar_jogo(data, estadio, id_clube_casa, id_clube_fora, golos_casa, golos_fora)

            if status == 201:
                print(f" Jogo no {dados['estadio']} adicionado!")
            else:
                logger.error("Erro ao adicionar jogo via menu — código %s: %s", status, dados)
                print(f" ERRO - {status}: {dados}")

        elif op == "15":
            status, dados = listar_jogos()

            if status in (200, 204):
                if isinstance(dados, str):
                    print(dados)
                else:
                    print("\n--- Jogos ---")
                    for j in dados:
                        print(f'{j["id_jogo"]} | {j["data"]} | {j["estadio"]} | {j["golos_casa"]}-{j["golos_fora"]}')
            else:
                logger.error("Erro ao listar jogos — código %s: %s", status, dados)
                print("", dados)

        elif op == "16":
            try:
                id_jogo = int(input("ID do jogo: "))
                status, jogo = obter_jogo(id_jogo)

                if status == 200:
                    print("\n--- Detalhes do Jogo ---")
                    for k, v in jogo.items():
                        print(f"{k}: {v}")
                else:
                    logger.error("Erro ao procurar jogo ID %s — código %s: %s", id_jogo, status, jogo)
                    print("", jogo)
            except ValueError:
                print(" ID inválido!")

        elif op == "17":
            try:
                id_jogo = int(input("ID do jogo: "))
            except ValueError:
                print(" ID inválido!")
                continue

            estadio = input("Novo estádio (ENTER para manter): ")
            golos_casa = input("Novos golos casa (ENTER para manter): ")
            golos_fora = input("Novos golos fora (ENTER para manter): ")

            status, msg = atualizar_jogo(
                id_jogo,
                int(golos_casa) if golos_casa else None,
                int(golos_fora) if golos_fora else None,
                estadio or None,
            )

            if status == 200:
                print(" Jogo atualizado!")
            else:
                logger.error("Erro ao atualizar jogo ID %s — código %s: %s", id_jogo, status, msg)
                print("", msg)

        elif op == "18":
            try:
                id_jogo = int(input("ID do jogo: "))
                status, dados = remover_jogo(id_jogo)

                if status == 200:
                    print(f" Jogo {dados['id_jogo']} removido!")
                else:
                    logger.error("Erro ao remover jogo ID %s — código %s: %s", id_jogo, status, dados)
                    print("", dados)
            except ValueError:
                print(" ID inválido!")

        elif op == "0":
            logger.info("Sistema encerrado pelo utilizador")
            print("A sair e o sporting vai ser tricampeão")
            break

        else:
            print(" Opção inválida!")


if __name__ == "__main__":
    main()
