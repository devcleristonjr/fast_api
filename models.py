# Importando os módulos necessários do SQLAlchemy, datetime e pytz
from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base #Base para criação dos modelos no banco de dados
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


# Definindo a classe Task que representa a tabela 'tasks' no banco de dados
class Task(Base):
    __tablename__ = 'tasks'  
    
    id = Column(Integer, primary_key=True)
    name = Column(String(150)) 
    description = Column(String(150))
    created_at = Column(DateTime, default=current_time)
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)
    progress = Column(String(50), default="open")

    def __repr__(self):
        return '<Task %r>' % (self.id)
