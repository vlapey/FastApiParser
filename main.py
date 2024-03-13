from html_helper import *

gender_category_pages = [
    {'name': "Мужское", 'href': "/c/17/shoes-men/"},
    {'name': "Женское", 'href': "/c/15/shoes-women/"},
    {'name': "Детям", 'href': "/c/5379/default-devochkam/"},
]


for gender_category in gender_category_pages:
    for category in get_gender_categories(gender_category['href']):
        for page in range(1, get_category_pages_count(category['href']) + 1):
            goods = get_page_goods(category['href'], page)
            # call db here
