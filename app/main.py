from fastapi import FastAPI, status, Query
from app.scraper import save_info, get_info  # Importa as funções do scraper

app = FastAPI()

# Endpoint para salvar informações no MongoDB
@app.post("/save_info/{item}", status_code=status.HTTP_201_CREATED)
async def save(item: str):
    return await save_info(item)

# Endpoint para obter informações do MongoDB
@app.get("/get_info/{item}")
async def get(item: str, min_price: float = Query(None), max_price: float = Query(None)):
    # Chama a função get_info do scraper com os parâmetros opcionais de Query
    return await get_info(item, min_price, max_price)

# Descrição da rota raiz
@app.get("/", tags=["Root"])
async def read_root():
    # Mensagem de boas-vindas e direcionamento para a documentação
    return {"message": "Bem-vindo à API de Scraping. Acesse /docs para a documentação da API."}

# Inicializa o servidor usando uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
