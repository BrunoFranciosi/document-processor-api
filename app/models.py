from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column("id", Integer, primary_key=True, index=True)
    nome = Column("nome", String, index=True, nullable=False)
    email = Column("email", String, unique=True, index=True, nullable=False)
    criado_em = Column("criado_em", DateTime, default=datetime.utcnow)


    documentos = relationship("Documento", back_populates="cliente", cascade="all, delete")



class Documento(Base):
    __tablename__ = "documentos"
    id = Column("id", Integer, primary_key=True, index=True)
    titulo = Column("titulo", String, index=True)
    conteudo = Column("conteudo", Text)
    processado_em = Column("processado_em", DateTime, default=datetime.utcnow)
    origem = Column("origem", String) # 'pdf' or 'web'
    nome_arquivo = Column("nome_arquivo", String, nullable=True)
    url = Column("url", String, nullable=True)
    cliente_id = Column("cliente_id", Integer, ForeignKey("clientes.id"))


    cliente = relationship("Cliente", back_populates="documentos")

    