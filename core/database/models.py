
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
    reviews_count = Column(Integer, default=0)
    rating = Column(Numeric(10, 1), default=0.0)

    authored_reviews = relationship('Review', back_populates='author', foreign_keys='Review.author_id')
    owned_reviews = relationship('Review', back_populates='seller', foreign_keys='Review.seller_id')
    chats_as_client = relationship('Chat', back_populates='client', foreign_keys='Chat.client_id')
    chats_as_seller = relationship('Chat', back_populates='seller', foreign_keys='Chat.seller_id')
    lots = relationship('Lot', back_populates='seller')
    sended_messages = relationship('Message', back_populates='sender')
    client_orders = relationship('Order', back_populates='client', foreign_keys='Order.client_id')
    selled_orders = relationship('Order', back_populates='seller', foreign_keys='Order.seller_id')

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('users.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))

    client = relationship('User', back_populates='chats_as_client', foreign_keys=[client_id])
    seller = relationship('User', back_populates='chats_as_seller', foreign_keys=[seller_id])
    messages = relationship('Message', back_populates='chat')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)

    chat = relationship('Chat', back_populates='messages')
    sender = relationship('User', back_populates='sended_messages')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    stars = Column(Integer, CheckConstraint('stars >= 1 AND stars <= 5'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='authored_reviews', foreign_keys=[author_id])
    seller = relationship('User', back_populates='owned_reviews', foreign_keys=[seller_id])

class Lot(Base):
    __tablename__ = 'lots'
    id = Column(Integer, primary_key=True)
    short_description = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), CheckConstraint('price >= 0.01'), nullable=False)
    stock = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'), index=True)
    seller_id = Column(Integer, ForeignKey('users.id'))
    buying_message = Column(String, nullable=True)

    category = relationship('Category', back_populates='lots')
    seller = relationship('User', back_populates='lots')
    orders = relationship('Order', back_populates='lot')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    lot_id = Column(Integer, ForeignKey('lots.id'))
    client_id = Column(Integer, ForeignKey('users.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='waiting')
    create_time = Column(DateTime, default=datetime.now)
    close_time = Column(DateTime, nullable=True)
    
    lot = relationship('Lot', back_populates='orders')
    client = relationship('User', back_populates='client_orders', foreign_keys=[client_id])
    seller = relationship('User', back_populates='selled_orders', foreign_keys=[seller_id])

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