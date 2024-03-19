import pymongo
from lamoda_helpers.html_helper import *

client = pymongo.MongoClient('mongodb://mongo:27017/')
db = client['lamoda_db']
collection = db['goods']

gender_category_pages = [
    {'name': "Мужское", 'href': "/c/17/shoes-men/"},
    {'name': "Женское", 'href': "/c/15/shoes-women/"},
    {'name': "Детям", 'href': "/c/5379/default-devochkam/"},
]


def parse():
    for gender_category in gender_category_pages:
        for category in get_gender_categories(gender_category['href']):
            for page in range(1, get_category_pages_count(category['href']) + 1):
                goods = get_page_goods(category['href'], page)
                collection.insert_many(goods)
            return get_products()


def get_products():
    products = list(collection.find({}, {"_id": False}))
    return products
