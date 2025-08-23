from app.database import Base, db
from app import models

print(" Criando tabelas...")
Base.metadata.create_all(bind=db)
print("Tabelas criadas!")
