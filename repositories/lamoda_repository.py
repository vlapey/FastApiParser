from lamoda_helpers.html_helper import *
from persistence.db_conn import LamodaDbConnection


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
                await LamodaDbConnection.collection.insert_many(goods)
                return await get_products()


async def get_products():
    products = await LamodaDbConnection.collection.find({}, {"_id": False}).to_list(length=None)
    return products
