from fastapi import FastAPI, status
from app.scraper import save_info, get_info  # Importa as funções do scraper

app = FastAPI()

# Endpoint para salvar informações no MongoDB
@app.get("/save_info/{item}", status_code=status.HTTP_201_CREATED)
async def save(item: str):
    return await save_info(item)

# Endpoint para obter informações do MongoDB
@app.get("/get_info/{item}")
async def get(item: str):
    return await get_info(item)

# Descrição da rota raiz
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API de Scraping. Acesse /docs para a documentação da API."}

# Inicializa o servidor usando uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
