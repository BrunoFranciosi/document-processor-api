from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from . import models, crud, database
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import io, requests
from sqlalchemy import func

# Cria tabelas no banco dentro do db CRIA TUDO NO BANCO DE DADOS 2 funcao
models.Base.metadata.create_all(bind=database.db)

# Criando a sessão global do banco
db = database.SessionLocal()



app = FastAPI()

#ROTAS @app.__("/")
@app.get("/")
def home():
    return "Processamento de Documentos API"

# CLIENTES

@app.post("/clientes/")
def criar_cliente(nome: str = Form(...), email: str = Form(...)):
    return crud.adicionar_cliente(db, nome, email)

@app.get("/clientes/")
def listar_clientes():
    return crud.listar_clientes(db)

@app.get("/clientes/{cliente_id}")
def buscar_cliente(cliente_id: int):
    cliente = crud.buscar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado") # O cliente da API vai receber um response HTTP 404 (status correto), vai recer um json certo, caso seja um return "Cliente não encontrado"  Isso não retorna um erro HTTP 404. O FastAPI vai retornar status 200 OK com um corpo: "Cliente não encontrado"
    return cliente

@app.put("/clientes/{cliente_id}")
def atualizar_cliente(cliente_id: int, nome: str = None, email: str = None):
    cliente = crud.atualizar_cliente(db, cliente_id, nome, email)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")
    return cliente

@app.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int):
    cliente = crud.deletar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")
    return {"detail": "Cliente deletado"}





# DOCUMENTOS

@app.post("/documentos/upload-pdf/")
def upload_pdf(cliente_id: int = Form(...), file: UploadFile = File(...)):
    cliente = crud.buscar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    conteudo_bytes = file.file.read()
    reader = PdfReader(io.BytesIO(conteudo_bytes))
    texto = "\n".join([p.extract_text() or "" for p in reader.pages])
    titulo = file.filename

    return crud.adicionar_documento(
        db, cliente_id, titulo, texto, origem="pdf", nome_arquivo=file.filename
    )

@app.post("/documentos/url/")
def documento_de_url(cliente_id: int = Form(...), url: str = Form(...)):
    cliente = crud.buscar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    titulo = url
    conteudo = "\n".join(p.get_text(strip=True) for p in soup.find_all("p")[:50])

    return crud.adicionar_documento(
        db, cliente_id, titulo, conteudo, origem="web", url=url
    )

# Listar todos os clientes com contagem de documentos
'''
@app.get("/clientes-com-contagem/")
def clientes_com_contagem():
    resultado = (
        db.query(
            models.Client,
            func.count(models.Document.id).label("qtd_documentos")
        )
        .outerjoin(models.Document, models.Document.cliente_id == models.Client.id)
        .group_by(models.Client.id)
        .all()
    )
    return [
        {"id": c.Client.id, "nome": c.Client.name, "email": c.Client.email, "qtd_documentos": c.qtd_documentos}
        for c in resultado
    ]
'''

# Listar todos os documentos de um cliente específico
@app.get("/clientes/{cliente_id}/documentos/")
def listar_documentos(cliente_id: int):
    return crud.listar_documentos_do_cliente(db, cliente_id)

# Buscar documentos por usuário (retornando campos específicos)
'''
@app.get("/documentos/buscar/")
def buscar_documentos(cliente_id: int = None, nome_cliente: str = None):
    query = db.query(models.Document, models.Client).join(models.Client)
    
    if cliente_id:
        query = query.filter(models.Document.cliente_id == cliente_id)
    if nome_cliente:
        query = query.filter(models.Client.name.ilike(f"%{nome_cliente}%"))
    
    resultados = query.all()
    return [
        {
            "documento_id": d.Document.id,
            "titulo": d.Document.titulo,
            "origem": d.Document.origem,
            "cliente_id": d.Client.id,
            "cliente_nome": d.Client.name
        }
        for d in resultados
    ]

'''
