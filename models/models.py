from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, deferred
from config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = deferred(Column(String, nullable=False))
    pin = Column(Integer)
    is_admin = Column(Boolean, nullable=False)
    buttons = relationship("Button", back_populates="user", cascade="all, delete-orphan")

class Button(Base):
    __tablename__ = "buttons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    image_path = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="buttons")
