from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, select, ARRAY, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pgvector.sqlalchemy import Vector
from pydantic import BaseModel
import datetime
from typing import Annotated

import uuid
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('POSTGRES_DB_URL')
PASS = os.getenv('POSTGRES_DB_PASS')

DATABASE_URL = f"postgresql://postgres:{PASS}@{URL}:5432/postgres"

Base = declarative_base()
engine = create_engine(DATABASE_URL,pool_pre_ping=True,pool_size=50, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Repository:
    def __init__(self, model):
        self.model = model

    def write(self, **kwargs):
        with SessionLocal() as db:
            instance = self.model(**kwargs)
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return instance
    
    def read_by_key(self, key, value):
        with SessionLocal() as db:
            return db.query(self.model).filter(getattr(self.model, key) == value).all()

    def read_by_primary_key(self, pk):
        with SessionLocal() as db:
            return db.query(self.model).get(pk)

    def read_all(self):
        with SessionLocal() as db:
            return db.query(self.model).all()
    
    def update(self, pk, **kwargs):
        with SessionLocal() as db:
            instance = db.query(self.model).get(pk)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                db.commit()
                db.refresh(instance)
            return instance

class Consultora(Base):
    __tablename__ = 'consultora'
    numero = Column(String, primary_key=True)
    nombre = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    buffer = Column(ARRAY(String), default=[])
    
class Pedidos(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String)
    numero = Column(String)
    fecha = Column(Date)
    cantidad = Column(Integer)
    nombre_vendio = Column(String)
    numero_vendio = Column(String)
