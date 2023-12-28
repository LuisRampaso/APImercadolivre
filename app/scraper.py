import requests
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
import os
import uuid

# Conexão com o MongoDB
MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client['items']
collection = db['items_01']

# Função para raspar dados do Mercado Livre
async def scrape_mercado_livre(url, min_price=None, max_price=None):
    try:
        # Obtém a página HTML
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        # Em caso de falha na solicitação, gera um erro específico HTTP
        raise HTTPException(status_code=400, detail=f"Failed to fetch data: {e}")

    # Parseia o HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')
    items = []

    # Encontra os elementos de interesse na página
    item_boxes = soup.find_all("div", class_="ui-search-result__content-wrapper")
    for index, item_box in enumerate(item_boxes, start=1):
        # Obtém o título do item
        title_element = item_box.find("h2", class_="ui-search-item__title")
        title = title_element.text.strip() if title_element else "Title not available"

        # Obtém o elemento do preço
        price_element = item_box.find("span", class_="andes-money-amount__fraction")
        price_text = price_element.text.strip() if price_element else "0.0"

        # Remove a pontuação dos preços e converte para float
        price_text = price_text.replace(".", "").replace(",", ".")
        price = float(price_text)  # Converte para float

        # Aplica filtros de preço, se fornecidos
        if (min_price is None or price >= min_price) and (max_price is None or price <= max_price):
            # Cria um dicionário com informações do item
            item_info = {
                'id': index,
                'title': title,
                'price': price,
            }
            items.append(item_info)

    return {
        'url': url,
        'items': items
    }

# Função para salvar informações no MongoDB
async def save_info(item: str, min_price: float = None, max_price: float = None):
    url = f'https://lista.mercadolivre.com.br/{item}'  # URL base do Mercado Livre

    data = await scrape_mercado_livre(url, min_price, max_price)

    await collection.insert_one(data)  # Insere os dados no MongoDB

    return {"Mensagem": "Itens Salvos Com Sucesso"}

# Função para obter informações do MongoDB
async def get_info(item: str, min_price: float = None, max_price: float = None):
    url = f'https://lista.mercadolivre.com.br/{item}'  # URL base do Mercado Livre

    data = await collection.find_one({'url': url})  # Busca os dados no MongoDB

    if not data:
        raise HTTPException(status_code=404, detail="Not Found")

    # Filtra e ordena os itens baseados nos parâmetros de preço, se fornecidos
    filtered_items = data.get("items", [])
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.get("price") >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.get("price") <= max_price]

    filtered_items.sort(key=lambda x: x.get("price"))  # Ordena os itens por preço

    return {"url": data.get("url"), "items": filtered_items}
