# 🟢 Sporting Clube de Portugal — Base de Dados de Gestão de Futebol

<div align="center">

![Sporting CP](https://img.shields.io/badge/Clube-Sporting%20CP-green?style=for-the-badge&logo=data:image/svg+xml;base64,)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)
![Tipo](https://img.shields.io/badge/Tipo-Base%20de%20Dados%20Relacional-blue?style=for-the-badge)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-lightgrey?style=for-the-badge)

**Modelo de base de dados relacional para gestão completa de um clube de futebol profissional.**

</div>

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Modelo de Dados](#modelo-de-dados)
  - [Entidades Principais](#entidades-principais)
  - [Relações](#relações)
- [Diagrama ER](#diagrama-er)
- [Estrutura das Entidades](#estrutura-das-entidades)
- [Tecnologias](#tecnologias)
- [Como Usar](#como-usar)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 📌 Sobre o Projeto

Este projeto consiste no desenho e implementação de uma **base de dados relacional** para a gestão operacional e desportiva do **Sporting Clube de Portugal**. O modelo contempla a gestão de jogadores, staff técnico, jogos, estádio, claques, orçamento, academia e muito mais — cobrindo todas as vertentes essenciais de um clube de futebol profissional moderno.

### Objetivos
- Modelar todas as entidades relevantes de um clube de futebol de forma estruturada
- Garantir integridade referencial entre entidades relacionadas
- Suportar consultas sobre desempenho de jogadores, resultados de jogos e gestão financeira
- Servir como base para futuras aplicações de gestão desportiva

---

## 🗄️ Modelo de Dados

### Entidades Principais

| # | Entidade | Descrição |
|---|----------|-----------|
| 1 | **Jogador** | Representa cada jogador da equipa, com dados pessoais, contratuais e desportivos |
| 2 | **Clube** | Informações institucionais do clube (nome, marca, NIF, ID) |
| 3 | **Staff** | Equipas de suporte — médica e tática |
| 4 | **Treinador** | Treinador(es) do clube, com dados profissionais e licença UEFA |
| 5 | **Estádio** | Capacidade total, dimensões e características do estádio |
| 6 | **Claque** | Identificação das claques, presença nos jogos e torcida |
| 7 | **Equipas** | Equipa principal, secundárias e jovens |
| 8 | **Academia** | Gestão dos treinos e jogadores em desenvolvimento |
| 9 | **Presidente** | Presidente atual, histórico de presidentes e mandatos |
| 10 | **Orçamento** | Gestão financeira mensal, anual e por prémios |
| 11 | **Sócios** | Número total de sócios e novos registos por ano |
| 12 | **Jogo** | Registo de jogos, com equipas, marcadores, golos e convocados |

---

## 🔗 Relações

```
Clube ──< Jogador          (1 clube tem vários jogadores)
Clube ──< Treinador        (1 clube tem 1 treinador principal)
Clube ──< Jogo             (2 clubes participam num jogo)
Jogador >──< Jogo          (jogadores participam em jogos — tabela associativa com estatísticas)
```

---

## 📐 Diagrama ER

```
┌─────────────────────┐        ┌──────────────────────┐
│       CLUBE         │        │       JOGADOR         │
├─────────────────────┤        ├──────────────────────┤
│ PK  id_clube        │◄──┐    │ PK  id_jogador        │
│     nome            │   └────│ FK  id_clube          │
│     marca           │        │     nome              │
│     nif             │        │     data_nascimento   │
└─────────────────────┘        │     posicao           │
         │                     │     numero_camisa     │
         │                     │     peso / altura     │
         ▼                     │     nacionalidade     │
┌─────────────────────┐        │     pe_preferido      │
│     TREINADOR       │        │     salario           │
├─────────────────────┤        │     inicio_contrato   │
│ PK  id_treinador    │        │     fim_contrato      │
│ FK  id_clube        │        │     clausula_rescisao │
│     nome            │        └──────────────────────┘
│     nacionalidade   │                   │
│     data_nascimento │                   │ N:M
│     licenca_UEFA    │                   ▼
└─────────────────────┘        ┌──────────────────────┐
                               │        JOGO           │
                               ├──────────────────────┤
                               │ PK  id_jogo           │
                               │     data              │
                               │     local_estadio     │
                               │     golos_casa        │
                               │     golos_fora        │
                               │ FK  id_clube_casa     │
                               │ FK  id_clube_fora     │
                               │     marcadores_ids    │
                               │     convocados_ids    │
                               └──────────────────────┘
```

---

## 📂 Estrutura das Entidades

<details>
<summary><strong>🧍 Jogador</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_jogador` | INT (PK) | Identificador único do jogador |
| `nome` | VARCHAR | Nome completo |
| `data_nascimento` | DATE | Data de nascimento |
| `posicao` | ENUM | Guarda-redes, Defesa, Médio, Avançado |
| `numero_camisa` | INT | Número na camisola |
| `id_clube` | INT (FK) | Referência ao clube |
| `peso` | DECIMAL | Peso em kg |
| `altura` | DECIMAL | Altura em cm |
| `nacionalidade` | VARCHAR | Nacionalidade |
| `pe_preferido` | ENUM | `Esquerdo`, `Direito`, `Ambidestro` |
| `salario` | DECIMAL | Salário mensal (€) |
| `inicio_contrato` | DATE | Data de início do contrato |
| `fim_contrato` | DATE | Data de fim do contrato |
| `clausula_rescisao` | DECIMAL | Valor da cláusula de rescisão (€) |

</details>

<details>
<summary><strong>🏛️ Clube</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_clube` | INT (PK) | Identificador único |
| `nome` | VARCHAR | Nome oficial do clube |
| `marca` | VARCHAR | Marca/identidade visual |
| `nif` | VARCHAR | Número de Identificação Fiscal |

</details>

<details>
<summary><strong>👔 Treinador</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_treinador` | INT (PK) | Identificador único |
| `nome` | VARCHAR | Nome completo |
| `nacionalidade` | VARCHAR | Nacionalidade |
| `data_nascimento` | DATE | Data de nascimento |
| `licenca_UEFA` | VARCHAR | Tipo de licença UEFA (A, Pro, etc.) |
| `id_clube` | INT (FK) | Clube onde treina |

</details>

<details>
<summary><strong>🏟️ Estádio</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_estadio` | INT (PK) | Identificador único |
| `capacidade_total` | INT | Total de adeptos que cabem no estádio |
| `tamanho` | VARCHAR | Dimensões do relvado (ex: 105m × 68m) |

</details>

<details>
<summary><strong>⚽ Jogo</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_jogo` | INT (PK) | Identificador único |
| `data` | DATETIME | Data e hora do jogo |
| `local_estadio` | VARCHAR | Local / nome do estádio |
| `golos_casa` | INT | Golos marcados pela equipa da casa |
| `golos_fora` | INT | Golos marcados pela equipa visitante |
| `id_clube_casa` | INT (FK) | Clube da casa |
| `id_clube_fora` | INT (FK) | Clube visitante |
| `lista_marcadores_ids` | JSON / Assoc. | IDs dos marcadores de golos |
| `lista_convocados_ids` | JSON / Assoc. | IDs dos jogadores convocados |

</details>

<details>
<summary><strong>📣 Claque</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_claque` | INT (PK) | Identificador único |
| `nome` | VARCHAR | Nome da claque |
| `presenca_jogo` | BOOLEAN | Presença confirmada num jogo |
| `torcida_jogo` | INT | Número de adeptos da claque no jogo |

</details>

<details>
<summary><strong>👥 Staff</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_staff` | INT (PK) | Identificador único |
| `tipo` | ENUM | `Equipa Médica`, `Equipa Tática` |
| `nome` | VARCHAR | Nome do membro |
| `cargo` | VARCHAR | Função exercida |

</details>

<details>
<summary><strong>🏆 Equipas</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_equipa` | INT (PK) | Identificador único |
| `tipo` | ENUM | `Principal`, `Secundária`, `Jovens` |
| `nome` | VARCHAR | Nome da equipa |

</details>

<details>
<summary><strong>🎓 Academia</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_academia` | INT (PK) | Identificador único |
| `tipo_treino` | VARCHAR | Descrição do tipo de treino |
| `jogadores_novos` | INT | Número de novos jogadores em formação |

</details>

<details>
<summary><strong>🤵 Presidente</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_presidente` | INT (PK) | Identificador único |
| `nome` | VARCHAR | Nome do presidente |
| `atual` | BOOLEAN | Indica se é o presidente em exercício |
| `anos_mandato` | INT | Total de anos como presidente |
| `total_presidentes` | INT | Número histórico total de presidentes |

</details>

<details>
<summary><strong>💰 Orçamento</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_orcamento` | INT (PK) | Identificador único |
| `orcamento_mensal` | DECIMAL | Orçamento por mês (€) |
| `orcamento_anual` | DECIMAL | Orçamento total por ano (€) |
| `orcamento_premios` | DECIMAL | Verba recebida por prémios importantes (€) |

</details>

<details>
<summary><strong>🎟️ Sócios</strong></summary>

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_socios` | INT (PK) | Identificador único do registo |
| `total_socios` | INT | Número total de sócios do clube |
| `novos_socios_ano` | INT | Novos sócios registados por ano |
| `ano` | YEAR | Ano de referência |

</details>

---

## 🛠️ Tecnologias

- ![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white) Linguagem de consulta estruturada
- ![MySQL](https://img.shields.io/badge/MySQL-00758F?style=flat&logo=mysql&logoColor=white) ou **PostgreSQL** como SGBD recomendado
- **Diagrama ER** — modelado com ferramentas como dbdiagram.io ou draw.io

---

## 🚀 Como Usar

### 1. Clonar o repositório
```bash
git clone https://github.com/teu-utilizador/sporting-cp-db.git
cd sporting-cp-db
```

### 2. Criar a base de dados
```sql
CREATE DATABASE sporting_cp;
USE sporting_cp;
```

### 3. Executar os scripts SQL
```bash
mysql -u root -p sporting_cp < schema.sql
mysql -u root -p sporting_cp < seed_data.sql
```

### 4. Testar com queries de exemplo
```sql
-- Listar todos os jogadores e posições
SELECT nome, posicao, numero_camisa FROM Jogador ORDER BY posicao;

-- Ver jogos realizados pelo Sporting CP
SELECT j.data, j.golos_casa, j.golos_fora
FROM Jogo j
WHERE j.id_clube_casa = 1 OR j.id_clube_fora = 1;

-- Jogadores com contrato a terminar em 2025
SELECT nome, fim_contrato FROM Jogador
WHERE fim_contrato <= '2025-12-31';
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faz **fork** do repositório
2. Cria um branch para a tua feature: `git checkout -b feature/nova-entidade`
3. Realiza as alterações e faz commit: `git commit -m "feat: adicionar entidade X"`
4. Faz push para o teu branch: `git push origin feature/nova-entidade`
5. Abre um **Pull Request**

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

<div align="center">

Feito com 💚 para o **Sporting Clube de Portugal**

</div>
