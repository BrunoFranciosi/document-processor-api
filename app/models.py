from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


# Modelo que representa a tabela clientes
class Cliente(Base):
    __tablename__ = "clientes"

    # colunas da tabela
    id = Column("id", Integer, primary_key=True, index=True)
    nome = Column("nome", String, index=True, nullable=False)
    email = Column("email", String, unique=True, index=True, nullable=False)
    criado_em = Column("criado_em", DateTime, default=datetime.utcnow)

    # relacionamento -> um cliente pode ter varios documentos
    documentos = relationship(
        "Documento",                                                            # modelo relacionado
        back_populates="cliente",                                               # nome do relacionamento no outro lado
        cascade="all, delete"                                                   # se deletar o cliente, deleta os documentos tambem
    )


# Modelo que representa a tabela documentos
class Documento(Base):
    __tablename__ = "documentos"

    id = Column("id", Integer, primary_key=True, index=True)
    titulo = Column("titulo", String, index=True)
    conteudo = Column("conteudo", Text)
    processado_em = Column("processado_em", DateTime, default=datetime.utcnow)
    origem = Column("origem", String)                                           # 'pdf' or 'web'                      
    nome_arquivo = Column("nome_arquivo", String, nullable=True) 
    url = Column("url", String, nullable=True)
    cliente_id = Column("cliente_id", Integer, ForeignKey("clientes.id"))       # FK para clientes

    # relacionamento -> cada documento pertence a um cliente
    cliente = relationship("Cliente", back_populates="documentos")

    