import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import filter_accessories
from utils import get_the_lowest_price_product
from utils import filter_irrelevant_products
from utils import print_products

# todo: handle the case when no results are displayed on the page
def get_products(soup):
    """
    parse the products from the page and return the relevant products only.
    """
    product_cards = soup.select('.product-item-info')[:10]
    products = []
    for product_card in product_cards:
        title = product_card.select_one('.product-item-link').text.strip()
        price = product_card.select_one('.price-box')
        if not price:  # skip products without price in shophive
            continue
        price = price.text.strip()
        img_url = product_card.find('img')['src']
        product_page_url = product_card.find('a', class_='product photo product-item-photo')['href']

        product = {
            'title': title,
            'price': price,
            'img_url': img_url,
            'product_page_url': product_page_url
        }
        products.append(product)
    return products


def main(product_name):
    query = product_name.replace(' ', '+')
    URL = f'https://www.shophive.com/catalogsearch/result/?q={query}'
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = get_products(soup)

    # temporarily printing the scraped products
    print_products(products)

    products = filter_accessories(products)
    products = filter_irrelevant_products(product_name, products)
    lowest_price_product = get_the_lowest_price_product(products)
    return lowest_price_product


if __name__=='__main__':
    product = main('iphone 14')
    print(product)