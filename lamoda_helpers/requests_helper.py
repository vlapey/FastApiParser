from bs4 import BeautifulSoup
import requests


def get_soup_by_url(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    return soup
