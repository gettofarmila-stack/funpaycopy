
from datetime import  datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    registered_at = Column(DateTime, default=datetime.now)
    balance = Column(Numeric(10, 2), default=0.00)
    password_hash = Column(String, nullable=False)