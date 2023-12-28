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


async def scrape_mercado_livre(url, min_price=None, max_price=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        # Em vez de imprimir, retorna um erro específico
        raise HTTPException(status_code=400, detail=f"Failed to fetch data: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')
    items = []

    item_boxes = soup.find_all("div", class_="ui-search-result__content-wrapper")
    for index, item_box in enumerate(item_boxes, start=1):
        title_element = item_box.find("h2", class_="ui-search-item__title")
        title = title_element.text.strip() if title_element else "Title not available"

        price_element = item_box.find("span", class_="andes-money-amount__fraction")
        price = float(price_element.text.strip()) if price_element else 0.0
        
        # Aplicar filtros de preço, se fornecidos
        if (min_price is None or price >= min_price) and (max_price is None or price <= max_price):
            # Utiliza o índice como ID ao invés de UUID
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



async def save_info(item: str, min_price: float = None, max_price: float = None):
    url = f'https://lista.mercadolivre.com.br/{item}'  # URL base do Mercado Livre

    data = await scrape_mercado_livre(url, min_price, max_price)

    await collection.insert_one(data)

    return {"Mensagem": "Itens Salvos Com Sucesso"}


async def get_info(item: str, min_price: float = None, max_price: float = None):
    url = f'https://lista.mercadolivre.com.br/{item}'  # URL base do Mercado Livre

    data = await collection.find_one({'url': url})

    if not data:
        raise HTTPException(status_code=404, detail="Not Found")

    # Filtra os itens baseados nos parâmetros de preço, se fornecidos
    filtered_items = data.get("items", [])
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.get("price") >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.get("price") <= max_price]

    return {"url": data.get("url"), "items": filtered_items}