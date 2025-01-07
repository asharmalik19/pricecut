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

        product_from_daraz = product_from_daraz_future.result()
        product_from_telemart = product_from_telemart_future.result()
        product_from_shophive = product_from_shophive_future.result()
        
        print(f'\n product returned from daraz {product_from_daraz}')
        print(f'\n product returned from telemart {product_from_telemart}')
        print(f'\n product returned from shophive {product_from_shophive}')