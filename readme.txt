FastAPI CRUD API - Task Management

Este é um projeto simples de uma API para gerenciar tarefas, desenvolvido utilizando FastAPI. O sistema permite criar, ler, atualizar e excluir tarefas, oferecendo um pequeno sistema CRUD (Create, Read, Update, Delete).

Funcionalidades:

Adicionar Tarefas: Crie novas tarefas com nome, descrição e status de progresso.
Visualizar Tarefas: Liste todas as tarefas ou visualize os detalhes de uma tarefa específica.
Editar Tarefas: Atualize informações como nome, descrição e status.
Excluir Tarefas: Remova tarefas do sistema.


Tecnologias Usadas:

FastAPI: Framework para construir APIs rápidas e eficientes.
Jinja2: Renderização de templates HTML.
SQLite: Banco de dados utilizado.
SQLAlchemy: ORM para manipulação do banco de dados.
Bootstrap: Para estilização básica do front-end.

Estrutura do Projeto:

main.py: Gerencia as rotas e a lógica principal da aplicação.
models.py: Define os modelos de dados, incluindo a tabela de tarefas.
database.py: Configuração do banco de dados SQLite.
templates/: Contém os templates HTML usados na interface.
base.html: Template base para reutilização de layout.
index.html: Página inicial com a lista de tarefas.
addnew.html: Formulário para adicionar novas tarefas.
edit.html: Formulário para editar tarefas existentes.
task_detail.html: Detalhes de uma tarefa.
task_not_found.html: Página de erro para tarefas não encontradas.

Como Rodar o Projeto:
Passo 1: Instalar Dependências

pip install -r requirements.txt

Passo 2: Rodar o Servidor
Para rodar o servidor, execute o comando abaixo:

uvicorn main:app --reload

Passo 3: Acessar a Aplicação
Agora, você pode acessar a aplicação no navegador, indo até o endereço:

http://127.0.0.1:8000


