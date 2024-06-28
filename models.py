from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from database import Base
import uuid

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True)
    age = Column(Integer)
    email = Column(String(100))
