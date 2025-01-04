# Importando os módulos necessários do SQLAlchemy para trabalhar com banco de dados
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL de conexão com o banco de dados SQLite
# O banco de dados será armazenado em um arquivo chamado 'fastapidb.sqlite3' no mesmo diretório
DB_URL = 'sqlite:///fastapidb.sqlite3'

# Criando a engine de conexão com o banco de dados usando a URL fornecida
# O parâmetro 'check_same_thread' é necessário para SQLite quando usado com multithreading (geralmente em apps web)
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

# Criando a sessão local para interagir com o banco de dados
# 'autocommit=False' significa que as transações precisam ser explicitamente commitadas
# 'autoflush=False' significa que as consultas não serão automaticamente feitas ao banco de dados
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando a base declarativa para as classes de modelo, permitindo que elas sejam mapeadas para o banco
Base = declarative_base()
