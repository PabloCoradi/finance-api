# Finance API

API REST para controle financeiro pessoal, com foco em gerenciamento de contas, gastos e cálculo de dívidas com juros mensais.

## Sobre o projeto

Esse projeto nasceu da intenção de ter um controle financeiro mais previsível: organizar despesas em múltiplas contas (cartão, conta corrente), monitorar valores a vencer e projetar cenários de juros e despesas futuras, funcionando como um extrato inteligente com histórico e planejamento.

Além do objetivo prático, o projeto também é um exercício de aprendizado: é o primeiro sistema que desenvolvo do zero com arquitetura em camadas, autenticação real e boas práticas de segurança, saindo de um mini-CRUD em MVC para uma API REST completa.

## Funcionalidades

- **Autenticação de usuários**: registro e login com senha criptografada (bcrypt) e autenticação via token JWT
- **Gestão de contas**: criação de contas do tipo cartão de crédito ou conta corrente, cada uma com sua própria taxa de juros
- **Gestão de gastos**: registro de gastos vinculados a uma conta específica, com valor, descrição e data
- **Segurança por dono**: cada usuário só pode visualizar e modificar suas próprias contas e gastos
- **(Em desenvolvimento)** Fechamento mensal automático, com cálculo de saldo devedor e aplicação de juros sobre valores em aberto

## Tecnologias utilizadas

- **Python 3.11**
- **FastAPI** — framework para construção da API REST
- **SQLAlchemy** — ORM para modelagem e persistência de dados
- **SQLite** — banco de dados relacional (preparado para migração futura a PostgreSQL)
- **Pydantic** — validação de dados de entrada e saída
- **Passlib + bcrypt** — hash seguro de senhas
- **python-jose** — geração e validação de tokens JWT
- **python-dotenv** — gerenciamento de variáveis de ambiente

## Modelagem e arquitetura

O sistema é organizado em torno de 4 entidades principais:

- **User**: usuário do sistema, dono de uma ou mais contas
- **Account**: representa uma conta financeira (cartão de crédito ou conta corrente), com sua própria taxa de juros
- **Expense**: um gasto individual, vinculado a uma conta específica
- **FinalBalance**: o fechamento de uma conta em um determinado mês/ano, usado para histórico e cálculo de juros acumulados

```
User (1) ──── (N) Account (1) ──── (N) Expense
                    │
                    └──── (N) FinalBalance
```

O código segue uma arquitetura em camadas, separando responsabilidades:

```
finance-api/
├── models/         # Definição das tabelas do banco (SQLAlchemy)
├── schemas/        # Formatos de entrada e saída da API (Pydantic)
├── services/       # Lógica de negócio e acesso ao banco
├── api/
│   ├── routers/    # Definição das rotas/endpoints
│   └── dependencies.py  # Autenticação e verificações reutilizáveis
├── db/             # Configuração de conexão com o banco
└── main.py         # Ponto de entrada da aplicação
```

Essa separação garante que, por exemplo, trocar o banco de dados (de SQLite para PostgreSQL) exija mudar apenas uma linha de configuração, sem afetar o restante do código.

## Como rodar o projeto localmente

### Pré-requisitos
- Python 3.11 ou superior instalado

### Passo a passo

1. Clone o repositório:
```bash
git clone https://github.com/PabloCoradi/finance-api.git
cd finance-api
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com uma chave secreta:
```
SECRET_KEY=sua-chave-secreta-aqui
```

5. Rode o servidor:
```bash
uvicorn main:app --reload
```

6. Acesse a documentação interativa da API em:
```
http://127.0.0.1:8000/docs
```

## Endpoints principais

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/register` | Cria um novo usuário |
| POST | `/auth/login` | Autentica e retorna um token JWT |
| GET | `/auth/me` | Retorna os dados do usuário autenticado |
| POST | `/accounts` | Cria uma nova conta |
| GET | `/accounts` | Lista as contas do usuário autenticado |
| GET | `/accounts/{id}` | Busca uma conta específica |
| PUT | `/accounts/{id}` | Edita uma conta |
| DELETE | `/accounts/{id}` | Remove uma conta |
| POST | `/accounts/{id}/expenses` | Registra um gasto em uma conta |
| GET | `/accounts/{id}/expenses` | Lista os gastos de uma conta |
| GET | `/accounts/{id}/expenses/{id}` | Busca um gasto específico |
| PUT | `/accounts/{id}/expenses/{id}` | Edita um gasto |
| DELETE | `/accounts/{id}/expenses/{id}` | Remove um gasto |

Todas as rotas de `/accounts` e `/expenses` exigem autenticação via token JWT (header `Authorization: Bearer <token>`).

## Status do projeto

Este é um projeto em desenvolvimento contínuo, criado com fins de aprendizado.

## Autor

Desenvolvido por Pablo Coradi como projeto de estudo, durante a graduação em Engenharia de Software.