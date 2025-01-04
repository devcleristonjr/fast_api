# Importando os módulos necessários do SQLAlchemy, datetime e pytz
from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base  # Base para criação dos modelos no banco de dados
from datetime import datetime
from sqlalchemy.orm import declarative_base
import enum
import pytz

# Criando a base para os modelos, que é usada para mapear as classes para as tabelas do banco
Base = declarative_base()

# Definindo o fuso horário para o Brasil (São Paulo)
br_timezone = pytz.timezone('America/Sao_Paulo')

# Obtendo a hora atual no fuso horário brasileiro
current_time = datetime.now(br_timezone)

# Definindo o status de progresso do usuário, utilizando o Enum
class ProgressStatus(enum.Enum):
    open = "open"  # Status "open" para indicar que o item está aberto
    in_progress = "in progress"  # Status "in progress" para indicar que o item está em andamento
    completed = "completed"  # Status "completed" para indicar que o item foi concluído

# Definindo a classe User que representa a tabela 'users' no banco de dados
class User(Base):
    __tablename__ = 'users'  # Nome da tabela no banco de dados

    # Definindo as colunas da tabela
    id = Column(Integer, primary_key=True)  # Coluna ID, chave primária
    name = Column(String(150))  # Coluna name, com limite de 150 caracteres
    description = Column(String(150))  # Coluna description, com limite de 150 caracteres

    # Coluna created_at, automaticamente definida como o horário atual quando o usuário é criado
    created_at = Column(DateTime, default=current_time)

    # Coluna updated_at, que é automaticamente atualizada sempre que o usuário é alterado
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)

    # Coluna progress, que usa o Enum ProgressStatus para definir o progresso do usuário
    progress = Column(Enum(ProgressStatus), default=ProgressStatus.open)

    # Método especial para representação da instância User, útil para debug
    def __repr__(self):
        return '<User %r>' % (self.id)
