from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from .base import BaseUsers

#create DB, tables
class UsersTableORM(BaseUsers):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    time = Column(DateTime, default=func.current_timestamp())