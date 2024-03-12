import json
from bs4 import BeautifulSoup
import requests

root_url = 'https://www.lamoda.ru'


def get_genders():
    main_html = requests.get(root_url)
    main_soup = BeautifulSoup(main_html.text, 'html.parser')
    header_list = []
    header_a_list = main_soup.find('div', class_='d-header-genders').findAll('a', class_='d-header-genders_link')

    for item in header_a_list:
        header = {
            'name': item.text,
            'href': item['href'],
        }

        header_list.append(header)

    return header_list


def get_gender_categories(gender):
    gender_page_html = requests.get(root_url + gender['href'])
    gender_soup = BeautifulSoup(gender_page_html.text, 'html.parser')

    nav_menu = gender_soup.find('nav', class_='d-header-topmenu')
    nav_menu_items = nav_menu.findAll('a', class_='d-header-topmenu-category__link')

    categories = []

    for item in nav_menu_items:
        category = {
            'name': item.text,
            'href': item['href'],
        }

        categories.append(category)

    return categories


def get_category_pages_count(category):
    category_page_html = requests.get(root_url + category['href'])
    category_soup = BeautifulSoup(category_page_html.text, 'html.parser')

    print(category_soup)

    script = next(x for x in category_soup.findAll('script') if x.text.find("var __NUXT__") != -1)

    start_index_of_pagination_section = script.text.find('"pagination":') + len('"pagination":')
    end_index_of_pagination_section = script.text.find('}', start_index_of_pagination_section) + 1
    json_string = script.text[start_index_of_pagination_section:end_index_of_pagination_section]

    # todo: вместо json использовать поиск по 'pages'
    json_object = json.loads(json_string)
    count_of_pages = int(json_object['pages'])

    return count_of_pages


def get_page_goods(categoryUrl, page):
    page_html = requests.get(root_url + categoryUrl + '&page=' + str(page))
    page_soup = BeautifulSoup(page_html.text, 'html.parser')

    cards = page_soup.findAll('div', class_='x-product-card__card')

    # remove
    # cards = [cards[0]]

    goods = []

    for card in cards:
        # here you can get product url or image or smth

        description = card.find('div', class_='x-product-card-description')

        price_element = description.find('div', class_='x-product-card-description__price-wrap')
        if not price_element:
            price_element = description.find('span', class_='x-product-card-description__price-new')
        if not price_element:
            price_element = description.find('span', class_='x-product-card-description__price-single')

        brand_element = description.find('div', class_='x-product-card-description__brand-name')
        name_element = description.find('div', class_='x-product-card-description__product-name')

        good = {
            'price': price_element.text.strip(),
            'brand': brand_element.text.strip(),
            'name': name_element.text.strip(),
        }

        goods.append(good)

    return goods


genders = get_genders()

# remove
genders = [genders[1]]

for gender in genders:
    gender_categories = get_gender_categories(gender)

    # remove
    gender_categories = [gender_categories[2]]

    for category in gender_categories:
        count_of_pages = get_category_pages_count(category)

        # remove
        # count_of_pages = 1

        for page in range (1, count_of_pages + 1):
            print("page " + str(page))
            goods = get_page_goods(category['href'], page)
            # call db here
            print(goods)
