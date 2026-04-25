
from datetime import  datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship


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
    is_admin = Column(Boolean, default=False)

    lots = relationship('Lot', back_populates='seller')

class Lot(Base):
    __tablename__ = 'lots'
    id = Column(Integer, primary_key=True)
    short_description = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), CheckConstraint('price >= 0.01'), nullable=False)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))

    category = relationship('Category', back_populates='lots')
    seller = relationship('User', back_populates='lots')

class MainCategory(Base):
    __tablename__ = 'main_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True) # Minecraft, Roblox, Fortnite
    
    subcategories = relationship('Category', back_populates='main_category')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) # Робуксы, ключи
    main_category_id = Column(Integer, ForeignKey('main_categories.id'), nullable=False)
    
    main_category = relationship('MainCategory', back_populates='subcategories')
    lots = relationship('Lot', back_populates='category')