from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("sqlite:///./meubanco.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

Base = declarative_base()