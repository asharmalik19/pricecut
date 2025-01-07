from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime
import time
from selenium.common.exceptions import NoSuchElementException
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils import filter_accessories
from utils import get_the_lowest_price_product
from utils import filter_irrelevant_products
from utils import print_products


def get_driver():   
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver

def check_for_products_availability(driver):
    # refreshes the page 2 times while checking its availability
    if 'Search No Result' in driver.page_source:
        print('no result found yet')
        driver.refresh()
        if 'Search No Result' in driver.page_source:
            print('no result found yet')
            driver.refresh()
            if 'Search No Result' in driver.page_source:
                print('no result found yet')
                return False
            else:
                print('result found after second refresh')
                return True
        else:
            print('products displayed after first refresh')
            return True
    else:
        print('results found without refreshing')
        return True

def get_products(soup):
    """
    parse the products from the page and return the relevant products only.
    """
    product_cards = soup.select('.gridItem--Yd0sa')[:10]
    products = []
    for product_card in product_cards:
        product = {
        'title': product_card.select_one('#id-title').text.strip(),
        'price': product_card.select_one('.current-price--Jklkc').text.strip(),
        'img_url': product_card.select_one('img#id-img')['src'],
        'product_page_url': product_card.select_one('#id-a-link')['href'][2:]
        }
        products.append(product)
    return products


def main(product_name):
    query = product_name.replace(' ', '+')
    URL = f'https://www.daraz.pk/catalog/?q={query}&_keyori=ss&from=input&spm=a2a0e.home.search.go.35e34076nguURZ'

    driver = get_driver()
    driver.get(URL)

    products_available = check_for_products_availability(driver)
    if not products_available:
        print(f'no products found for {product_name}')
        driver.quit()
        return None
    
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")  # scrolling and wait is essential to tackle the lazy loading
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
    product = main('iphone 14')
    print(product)
