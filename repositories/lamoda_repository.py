import os

from lamoda_helpers.html_helper import *
from persistence.db_conn import LamodaMongoConnection
from persistence.db_conn import redis_pool
import pickle


gender_category_pages = [
    {'name': "Мужское", 'href': "/c/17/shoes-men/"},
    {'name': "Женское", 'href': "/c/15/shoes-women/"},
    {'name': "Детям", 'href': "/c/5379/default-devochkam/"},
]


async def parse():
    for gender_category in gender_category_pages:
        for category in get_gender_categories(gender_category['href']):
            for page in range(1, get_category_pages_count(category['href']) + 1):
                goods = get_page_goods(category['href'], page)
                await LamodaMongoConnection.collection.insert_many(goods)
                return await get_products()


async def get_products():
    cached_data = await get_cached_data()
    if cached_data:
        return cached_data

    products = await LamodaMongoConnection.collection.find({}, {"_id": False}).to_list(length=None)
    await cache_data(products)
    return products


async def get_cached_data():
    cached_data = await redis_pool.get('goods')
    if cached_data:
        return pickle.loads(cached_data)

    return None


async def cache_data(data):
    await redis_pool.set('goods', pickle.dumps(data), ex=os.getenv('DEFAULT_CACHE_EXPIRATION'))
    await redis_pool.aclose()
    return data

