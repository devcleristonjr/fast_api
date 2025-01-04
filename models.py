from sqlalchemy import Column, Integer, String,DateTime
from database import Base
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()
 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    description = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow)  # Automatically set when created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Automatically updated
 
    def __repr__(self):
        return '<User %r>' % (self.id)