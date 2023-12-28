# Web Scraper e API FastAPI para Salvamento e Recuperação de Itens do Mercado Livre

Este projeto é uma aplicação FastAPI para realizar scraping de itens do site Mercado Livre e salvar os dados em um banco de dados MongoDB.

## Funcionalidades

- **save_info:** Endpoint para realizar o scraping de itens a partir de uma URL fornecida e salvar os dados no MongoDB.

Exemplo de Uso do Endpoint /save_info
Para salvar informações de itens do site do Mercado Livre, utilize o seguinte formato de URL para fazer uma requisição GET:

http://localhost:8000/save_info/item_desejado

- **get_info:** Endpoint para obter os itens salvos no MongoDB a partir de uma URL fornecida.

Exemplo de Uso do Endpoint /get_info
Para obter as informações de itens previamente salvos do site do Mercado Livre, utilize o seguinte formato de URL para fazer uma requisição GET:

http://localhost:8000/get_info/item_desejado

Isso fará uma chamada ao endpoint /get_info, enviando a URL do item desejado como parâmetro.

## Configuração

1. Instale as dependências do projeto:
pip install -r requirements.txt



2. Defina as variáveis de ambiente no arquivo `.env`:
MONGODB_URL=sua_url_de_conexao_mongodb



3. Execute o servidor localmente:
uvicorn app.main:app --reload


## Estrutura do Projeto

projeto/
├── app/
│   ├── init.py
│   ├── main.py
│   └── scraper.py
├── .env
├── README.md
└── requirements.txt

- **`app/`:** Contém o código principal da aplicação.
- **`main.py`:** Arquivo principal da aplicação FastAPI.
- **`scraper.py`:** Contém funções relacionadas ao scraping de itens.
- **`.env`:** Arquivo de variáveis de ambiente (não deve ser enviado para o repositório).
- **`README.md`:** Este arquivo que contém informações sobre o projeto.

## Contribuição

- Sinta-se à vontade para contribuir com melhorias ou correções de bugs.
