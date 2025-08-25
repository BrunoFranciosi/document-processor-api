from fastapi.testclient import TestClient
from app.main import app

# Criar um cliente de teste que simula chamadas HTTP à API
client = TestClient(app)

def test_home():
    # Fazer uma requisição GET para a rota raiz "/"
    response = client.get("/")

    # Verificar se o status HTTP retornado é 200 (sucesso)
    assert response.status_code == 200

    # Verificar se o texto esperado aparece na resposta
    assert "Processamento de Documentos API" in response.text

def test_criar_e_listar_cliente():
    # Criar cliente

    # Enviar uma requisição POST para /clientes/
    # passando nome e email no corpo da requisição
    response = client.post("/clientes/", data={"nome": "Bruno", "email": "bruno@example.com"})
    assert response.status_code == 200
    cliente = response.json()
    assert cliente["nome"] == "Bruno"
    
    # Listar clientes
    response = client.get("/clientes/")
    assert response.status_code == 200
    clientes = response.json()
    assert any(c["email"] == "bruno@example.com" for c in clientes)