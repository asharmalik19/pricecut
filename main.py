from daraz_scraper import main as daraz_main
from shophive_scraper import main as shophive_main
from telemart_scraper import main as telemart_main
from concurrent.futures import ThreadPoolExecutor


if __name__=='__main__':
    query = 'samsung galaxy s22'

    with ThreadPoolExecutor(max_workers=3) as executor:
        product_from_daraz_future = executor.submit(daraz_main, query)
        product_from_telemart_future = executor.submit(telemart_main, query)
        product_from_shophive_future = executor.submit(shophive_main, query)   
        results = {
            'Daraz': product_from_daraz_future.result(),
            'Telemart': product_from_telemart_future.result(), 
            'Shophive': product_from_shophive_future.result()
        }
        for store, products in results.items():
            print(f'\nProducts returned from {store}: {products}')