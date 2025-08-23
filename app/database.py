from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("postgresql://postgres:root@127.0.0.1:5432/document_processor")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
Base = declarative_base()