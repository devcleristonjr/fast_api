from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
from datetime import datetime
from sqlalchemy.orm import declarative_base
import enum
import pytz

Base = declarative_base()

br_timezone = pytz.timezone('America/Sao_Paulo')

current_time = datetime.now(br_timezone)

class ProgressStatus(enum.Enum):
    open = "open" 
    in_progress = "in progress" 
    completed = "completed"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    description = Column(String(150))
    # Automatically set when created
    created_at = Column(DateTime, default=current_time)
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)  # Automatically updated
    progress = Column(Enum(ProgressStatus), default=ProgressStatus.open)

    def __repr__(self):
        return '<User %r>' % (self.id)
