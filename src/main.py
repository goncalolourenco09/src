from clube import (
    remover_clube,
    criar_clube,
    listar_clubes,
)
from jogador import (
    criar_jogador,
    listar_jogadores,
    remover_jogador,
    obter_jogador,
    atualizar_jogador,
)

def main():
    while True:
        print("""
    1. Adicionar 
    2. Listar 
    3. Procurar
    4. Atualizar
    5. Remover 
    6. Adicionar clube
    7. Remover clube
    8. listar clube
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
                print(f" ERRO - {status}: {dados}")

        elif op == "2":
            status, dados = listar_jogadores()

            if status == 200:
                print("\n--- Jogadores ---")
                for j in dados:
                    print(f'{j["id_jogador"]} | {j["nome"]} | Nº {j["numero_camisa"]}')
            else:
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

            status, msg = atualizar_jogador(id_jogador, nome, numero)

            if status == 200:
                print(" Jogador atualizado!")
            else:
                print("", msg)

        elif op == "5":
            try:
                id_jogador = int(input("ID: "))
                status, dados = remover_jogador(id_jogador)

                if status == 200:
                    print(" Jogador removido:", dados["nome"])
                else:
                    print("", dados)
            except ValueError:
                print(" ID inválido!")

        elif op == "6":
            nome = input("Nome do clube: ")
            nif = input("NIF: ")

            status, dados = criar_clube(nome, nif)

            if status == 200:
                print(" Clube criado:", dados["nome"])
            else:
                print("", dados)

        elif op == "7":
            try:
                id_clube = int(input("ID do clube: "))
                status, dados = remover_clube(id_clube)

                if status == 200:
                    print(" Clube removido:", dados["nome"])
                else:
                    print("", dados)
            except ValueError:
                print(" ID inválido!")

        elif op == "8":
            status, dados = listar_clubes()

            if status == 200:
                print("\n--- Clubes ---")
                if isinstance(dados, str):
                    print("", dados)
                else:
                    for c in dados:
                        print(f'{c["id_clube"]} | {c["nome"]} | NIF: {c["nif"]}')
            else:
                print("", dados)

        elif op == "0":
            print("A sair e o sporting vai ser tricampeão")
            break

        else:
            print(" Opção inválida!")


if __name__ == "__main__":
    main()