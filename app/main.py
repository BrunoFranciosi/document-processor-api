from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from . import models, crud, database
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import io, requests
from sqlalchemy import func

# Cria as tabelas no banco se ainda nao existirem
models.Base.metadata.create_all(bind=database.db)

# Instancia a sessao do banco de dados
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
        raise HTTPException(404, "Cliente não encontrado")
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

# Upload de arquivo PDF
@app.post("/documentos/upload-pdf/")
def upload_pdf(cliente_id: int = Form(...), file: UploadFile = File(...)):
    cliente = crud.buscar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    # Le o conteúdo do PDF
    conteudo_bytes = file.file.read()
    reader = PdfReader(io.BytesIO(conteudo_bytes))
    texto = "\n".join([p.extract_text() or "" for p in reader.pages])
    titulo = file.filename

    # Salva no banco como documento
    return crud.adicionar_documento(
        db, cliente_id, titulo, texto, origem="pdf", nome_arquivo=file.filename
    )

# Captura documento a partir de uma URL
@app.post("/documentos/url/")
def documento_de_url(cliente_id: int = Form(...), url: str = Form(...)):
    cliente = crud.buscar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    # Faz requisição da página e extrai os <p>
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    titulo = url
    conteudo = "\n".join(p.get_text(strip=True) for p in soup.find_all("p")[:50])

    return crud.adicionar_documento(
        db, cliente_id, titulo, conteudo, origem="web", url=url
    )

# Listar todos os clientes com contagem de documentos
@app.get("/clientes-com-contagem/")
def clientes_com_contagem():
    resultado = (
        db.query(
            models.Cliente,
            func.count(models.Documento.id).label("qtd_documentos")
        )
        .outerjoin(models.Documento, models.Documento.cliente_id == models.Cliente.id)
        .group_by(models.Cliente.id)
        .all()
    )
    return [
        {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "qtd_documentos": qtd_documentos
        }
        for cliente, qtd_documentos in resultado
    ]



# Listar todos os documentos de um cliente específico
@app.get("/clientes/{cliente_id}/documentos/")
def listar_documentos(cliente_id: int):
    return crud.listar_documentos_do_cliente(db, cliente_id)

# Buscar documentos por usuário (retornando campos específicos)
@app.get("/documentos/buscar/")
def buscar_documentos(cliente_id: int = None, nome_cliente: str = None):
    query = db.query(models.Documento, models.Cliente).join(models.Cliente)
    
    # Filtro por ID de cliente
    if cliente_id:
        query = query.filter(models.Documento.cliente_id == cliente_id)
    # Filtro por nome do cliente
    if nome_cliente:
        query = query.filter(models.Cliente.nome.ilike(f"%{nome_cliente}%"))
    
    resultados = query.all()
    
    # Retorna informações resumidas do documento + cliente
    return [
        {
            "documento_id": documento.id,
            "titulo": documento.titulo,
            "origem": documento.origem,
            "cliente_id": cliente.id,
            "cliente_nome": cliente.nome
        }
        for documento, cliente in resultados
    ]


