from fastapi import FastAPI
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = FastAPI()

client = MongoClient('mongodb://mongo:27017')
db = client['lamoda_positions']
collection = db['positions']


async def scrape_lamoda():
    url = 'https://www.lamoda.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all('div', class_='good-tile')

    parsed_data = []

    for product in products:
        name = product.find('h2', class_='name').text.strip()
        price = product.find('div', class_='price').text.strip()

        parsed_data.append({'name': name, 'price': price})

    return parsed_data


@app.get("/products")
async def get_products():
    data = await scrape_lamoda()
    return data

