from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime
import time
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from utils import filter_accessories
from utils import get_the_lowest_price_product
from utils import filter_irrelevant_products
from utils import print_products


def get_products(soup):
    """
    parse the products from the page and return the relevant products only.
    """
    BASE_URL = 'https://telemart.pk'
    product_cards = soup.find_all('div', {'class': 'bg-white relative cursor-pointer p-0.5 col-span-3'})[:10]
    products = []
    for product_card in product_cards: 
        product = {         
            'title': product_card.find('h4').text.strip(),          
            'price': product_card.find('span', class_='inline-block tracking-tighter roboto-new font-normal product-title-size mt-1 text-green-600').text.strip(),
            'img_url': product_card.find('img')['src'],
            'product_page_url': BASE_URL + product_card.find('a')['href'],
        }
        products.append(product)
    return products


def get_driver():   
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver


def main(product_name):
    query = product_name.replace(' ', '%20')
    URL = f'https://telemart.pk/search?query={query}'
    driver = get_driver()
    driver.get(URL)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="bg-white relative cursor-pointer p-0.5 col-span-3"]')))
    except TimeoutException as e:
        print(f'no products found for {product_name} on telemart')
        driver.quit()
        return None

    time.sleep(2)  # telemart displays irrelevant products for a moment before showing real result
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = get_products(soup)
    driver.quit()

    # temporarily printing the scraped products
    print_products(products)

    products = filter_accessories(products)
    products = filter_irrelevant_products(product_name, products)
    lowest_price_product = get_the_lowest_price_product(products)
    return lowest_price_product


if __name__=='__main__':
    product = main('realme note 50')
    print(product)