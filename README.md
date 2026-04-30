 Nome da equipa: Sporting Clube de Portugal
  
Tema: Equipa de futebol

Entidade:1. Jogador
Representa os jogadores da equipa.
Atributos:
id_jogador


nome


data de nascimento


posição


número_camisa


id_equipa
Peso e altura
nacionalidade
pé preferido(esquerdo,direto ambi destro)
salario
data do inicio do contrato e fim
clasua de rescisao

2. clube
Representa a equipa de futebol.
Atributos:
Marca


nome


Nif


ID



3:staff
equipa medica
equipa tatica



4:estadio
total de capacidade de adetpos que cabe dentro do estadio
tamanho do estadio


5:claque
nomes de claques
claque em cada jogo
torcida no jogo



6:equipas
equipa principal
equipas secundárias
equipa jovens



7:academia
treino
jogadores novos








8:presidente
presidente atual
total de presidentes
quantos anos ficou como presidente

9:orçamento
orçamento por mes
orçamento por ganhar premios importantes
orçamento por ano

10:numero de socios
numero de socios total do clube
numeros de novos socios por ano

Relação:

Uma equipa tem vários jogadores


Um jogador pertence a uma equipa


3 Treinador 
id_treinador
nome
nacionalidade
data_nascimento
licença_UEFA 
id_clube 

4 Jogo 
id_jogo
data
local / estádio
lista_marcadores_ids
golos_casa
golos_fora
id_clube_casa
id_clube_fora
lista de_jogadores_id convocados


Entidade
Relação
Treinador → Clube
Um clube tem um treinador




Jogo → Clube
Dois clubes participam num jogo
Jogadores → Jogo
Jogadores participam em jogos (tabela associativa com estatísticas)





consultar treinador por clube e consultar jogador por clube
