from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base() 

class Person(Base):
    __tablename__ = "person"    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phones = relationship("Phones", cascade="all, delete", backref="person")
    birthday = Column(DateTime, nullable=True) 

class Phones(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone = Column(Integer)
    person_id = Column(Integer, ForeignKey('person.id', ondelete="CASCADE")) 