from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cria a conexao com o banco de dados SQLite
db = create_engine("sqlite:///./meubanco.db")

# Cria uma sessão para interagir com o bando
SessionLocal = sessionmaker(bind=db)

# Base usada para definir os modelos(tabelas)
Base = declarative_base()