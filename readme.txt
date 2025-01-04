FastAPI CRUD (Create, Read, Update, Delete)


Este é um projeto simples feito com FastAPI para demonstrar operações básicas de CRUD (Criar, Ler, Atualizar e Deletar) em um banco de dados SQLite. O projeto possui uma interface web construída com HTML e Bootstrap para facilitar o gerenciamento de usuários.

Tecnologias Usadas:

FastAPI: Framework para construir APIs rápidas e eficientes.
SQLAlchemy: ORM para interação com o banco de dados.
SQLite: Banco de dados usado para armazenar os dados dos usuários.
Jinja2: Template engine para gerar HTML dinâmico.
Bootstrap: Framework CSS para deixar a interface mais bonita e responsiva.

Como Funciona:

O projeto permite realizar as seguintes ações sobre os usuários:

Criar: Adicionar novos usuários com nome, descrição e status de progresso.
Ler: Visualizar a lista de usuários cadastrados e detalhes de cada um.
Atualizar: Editar as informações de um usuário existente.
Deletar: Remover um usuário do banco de dados.

Estrutura do Projeto:

main.py: O arquivo principal que contém as rotas e a lógica da aplicação.
models.py: Definições das tabelas do banco de dados com SQLAlchemy.
database.py: Configuração do banco de dados e criação da sessão.
templates/: Contém os arquivos HTML (Jinja2 templates) para a interface web.
static/: Contém arquivos estáticos como CSS,

Como Rodar o Projeto
Passo 1: Instalar Dependências
Clone o repositório ou baixe os arquivos do projeto. Depois, instale as dependências necessárias com o seguinte comando:

pip install fastapi[all] sqlalchemy jinja2 uvicorn[standard]

Passo 2: Rodar o Servidor
Para rodar o servidor, execute o comando abaixo:

uvicorn main:app --reload

Passo 3: Acessar a Aplicação
Agora, você pode acessar a aplicação no navegador, indo até o endereço:

http://127.0.0.1:8000


Como Funciona o Código:

FastAPI gerencia as rotas da aplicação.

GET /: Exibe a lista de usuários cadastrados.
POST /add: Adiciona um novo usuário ao banco de dados.
GET /user/{user_id}: Exibe os detalhes de um usuário específico.
GET /edit/{user_id}: Permite editar as informações de um usuário.
POST /update/{user_id}: Atualiza as informações de um usuário.
GET /delete/{user_id}: Deleta um usuário.
SQLAlchemy é usado para criar as tabelas e manipular os dados no banco SQLite. O modelo User possui campos como name, description, created_at, updated_at e progress, que são armazenados no banco.

Jinja2 gera os arquivos HTML dinamicamente com os dados do banco.

Estrutura de Banco de Dados
A tabela users tem os seguintes campos:

id: Identificador único do usuário (auto incrementado).
name: Nome do usuário.
description: Descrição do usuário.
created_at: Data e hora de criação.
updated_at: Data e hora da última atualização.
progress: Status do progresso (open, in progress, completed).

