# Imagem do python
FROM python:3.11-slim

# hey docker start from this point, go to de app directory, nosso codigo ta la
WORKDIR /app


COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]