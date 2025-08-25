from sqlalchemy.orm import Session
from . import models

# CLIENTES
def adicionar_cliente(db: Session, nome: str, email: str):
    '''
    Cria e adiciona um novo cliente no bando de dados
    '''
    cliente = models.Cliente(nome=nome, email=email)
    db.add(cliente)
    db.commit()             # confima a insercao no banco
    db.refresh(cliente)     # força o SQLAlchemy a recarregar o objeto inteiro do banco
    return cliente

def listar_clientes(db: Session):
    '''
    Retorna todos os clientes cadastrados
    '''
    return db.query(models.Cliente).all()

def buscar_cliente(db: Session, cliente_id: int):
    '''
    Busca um cliente pelo ID
    '''
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def atualizar_cliente(db: Session, cliente_id: int, nome: str = None, email: str = None):
    '''
    Atualiza os dados de um cliente (nome/email)
    '''
    cliente = buscar_cliente(db, cliente_id)
    if not cliente:
        return None
    if nome:
        cliente.nome = nome
    if email:
        cliente.email = email
    db.commit()
    db.refresh(cliente)
    return cliente

def deletar_cliente(db: Session, cliente_id: int):
    '''
    Remove um cliente do banco de dados
    '''
    cliente = buscar_cliente(db, cliente_id)
    if not cliente:
        return None
    db.delete(cliente)
    db.commit()
    return cliente


# DOCUMENTOS
def adicionar_documento(db: Session, cliente_id: int, titulo: str, conteudo: str, origem: str, nome_arquivo: str = None, url: str = None):
    '''
    Cria e associa um documento('pdf' ou 'web') a um cliente existente
    '''
    documento = models.Documento(
        cliente_id=cliente_id,
        titulo=titulo,
        conteudo=conteudo,
        origem=origem,
        nome_arquivo=nome_arquivo,
        url=url
    )
    db.add(documento)
    db.commit()
    db.refresh(documento)
    return documento

def listar_documentos_do_cliente(db: Session, cliente_id: int):
    '''
    Lista todos os documentos associados a um cliente
    '''
    return db.query(models.Documento).filter(models.Documento.cliente_id == cliente_id).all()
