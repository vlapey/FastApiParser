from requests_helper import *
from json_helper import *

root_url = 'https://www.lamoda.by'


def get_gender_categories(gender_url):
    gender_page_url = root_url + gender_url
    gender_soup = get_soup_by_url(gender_page_url)
    script = get_script_with_page_state_json(gender_soup)

    json_string = get_json_string_by_marker_string(script, '"category_tree":', ',"sort"')
    categories = get_categories_from_json_string(json_string)

    return categories


def get_category_pages_count(category_url):
    category_page_url = root_url + category_url
    category_soup = get_soup_by_url(category_page_url)

    script = get_script_with_page_state_json(category_soup)

    json_string = get_json_string_by_marker_string(script, '"pagination":', '}', 1)
    count_of_pages = get_count_of_pages_from_json_string(json_string)

    return count_of_pages


def get_price_by_description_element(description):
    price_element = description.find('div', class_='x-product-card-description__price-wrap')
    if not price_element:
        price_element = description.find('span', class_='x-product-card-description__price-new')
    if not price_element:
        price_element = description.find('span', class_='x-product-card-description__price-single')

    return price_element.text.strip()


def get_brand_by_description_element(description):
    brand_element = description.find('div', class_='x-product-card-description__brand-name')

    return brand_element.text.strip()


def get_name_by_description_element(description):
    name_element = description.find('div', class_='x-product-card-description__product-name')

    return name_element.text.strip()


def get_page_goods(category_url, page):
    page_url = root_url + category_url + '?sitelink=topmenuM&l=4&page=' + str(page)
    page_soup = get_soup_by_url(page_url)

    cards = page_soup.findAll('div', class_='x-product-card__card')

    goods = []

    for card in cards:
        # here you can get product url or image or smth
        description = card.find('div', class_='x-product-card-description')

        good = {
            'price': get_price_by_description_element(description),
            'brand': get_brand_by_description_element(description),
            'name': get_name_by_description_element(description),
        }

        goods.append(good)

    return goods
