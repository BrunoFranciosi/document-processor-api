import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, crud
from app.database import Base

# Criar um banco de dados em memória (só existe enquanto o teste roda).
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def test_adicionar_cliente():
    # Abrir sessão manualmente
    db = TestingSessionLocal()
    try:
        # Chamar a função do CRUD para adicionar um cliente no banco
        cliente = crud.adicionar_cliente(db, "Lucas", "lucas@example.com")

        # Verificar se o cliente realmente foi criado:
        assert cliente.id is not None
        assert cliente.nome == "Lucas"
        assert cliente.email == "lucas@example.com"
    finally:
        # Fechar a sessão do banco
        db.close()