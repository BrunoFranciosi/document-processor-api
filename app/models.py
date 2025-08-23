from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)


    documentos = relationship('Documento', back_populates='cliente')


class Documento(Base):
    __tablename__ = 'documentos'
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    conteudo = Column(Text)
    processado_em = Column(DateTime, default=datetime.utcnow)
    origem = Column(String) # 'pdf' or 'web'
    nome_arquivo = Column(String, nullable=True)
    url = Column(String, nullable=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))


    cliente = relationship('Cliente', back_populates='documentos')