from sqlalchemy import Column, String

from app.db import Base


class User(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    password = Column(String, nullable=False)
