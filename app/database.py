from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("sqlite:///./meubanco.db")
SessionLocal = sessionmaker(bind=db, autocommit=False, autoflush=False)

Base = declarative_base()