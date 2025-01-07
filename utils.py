import re

def filter_accessories(products):
    with open('accessories.txt', 'r') as file:
        accessories = [line.strip() for line in file.readlines()]
    filtered_products = []
    for product in products:
        is_accessory = False
        for accessory in accessories:
            if accessory.lower() in product['title'].lower():
                is_accessory = True
                print(f'accessory removed: {product["title"]}')
                break
        if not is_accessory:
            filtered_products.append(product)
    return filtered_products

# todo: This function also removes the phones which contains titles such 'iphone with free cover' etc, which needs a fix
def filter_irrelevant_products(product_name, products):
    filtered_products = []
    for product in products:
        if product_name.lower() in product['title'].lower():
            filtered_products.append(product)
        else:
            print(f'irrelevant product removed: {product["title"]}')
    return filtered_products



def convert_price_to_number(price_str):
    """
    Convert a price string to a numeric value.
    Extract the first floating-point number found in the string.
    Return None if the given price string has not matching pattern. Its true if the price is less than 1000.
    """
    price_match = re.search(r'\d+\,\d+', price_str)
    if price_match:
        price = price_match.group().replace(',', '')
        return float(price)
    else:
        return None


def get_the_lowest_price_product(products):
    """
    Find the product with the lowest price in the list of products.
    Returns None if an empty list of products is passed.
    """
    lowest_price = float('inf')  # Initialize with positive infinity
    lowest_price_product = None

    for product in products:
        price = convert_price_to_number(product['price'])
        if price is None:  # If a product price doesn't match the set pattern, skip it
            continue
        if price < lowest_price:
            lowest_price = price
            lowest_price_product = product
    
    return lowest_price_product  # The price in the returned product is in the original form as given


def print_products(products):
    for product in products:
        print(product['title'])


if __name__ == '__main__':

    product_name = 'iphone 14'
    products =  [{'title': 'Apple IPhone 14 128GB PTA Approved', 'price': 'Special Price Rs 294,999.00     was Rs 334,999.00', 'img_url': 'https://www.shophive.com/media/catalog/product/cache/3875881abdd255ac261538b8462285e9/i/m/image-removebg-preview---2022-09-08t163953.577_6_3.jpg', 'product_page_url': 'https://www.shophive.com/apple-iphone-14-128gb-pta-approved/'}, {'title': 'Apple IPhone 14 Pro 128GB PTA Approved', 'price': 'Rs 479,999.00', 'img_url': 'https://www.shophive.com/media/catalog/product/cache/3875881abdd255ac261538b8462285e9/i/p/iphone-14-pro-applestore.pk__5_1.jpg', 'product_page_url': 'https://www.shophive.com/apple-iphone-14-pro-128gb-pta-approved/'}]

    print(filter_irrelevant_products(product_name, products))