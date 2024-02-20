from bs4 import BeautifulSoup
import yaml
import requests

url = "https://jeulin.com/jeulin_fr/enseignement/physique-chimie.html"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    product_data = []

    for product_item in soup.find_all('li', class_='item product product-item simple'):
        product_info = {}

        sku_element = product_item.find('span', class_='product-item-sku')
        if sku_element is not None:
            product_info['sku'] = sku_element.find('span').text.strip()
        else:
            product_info['sku'] = 'N/A'

        product_info['name'] = product_item.find('h2', class_='product name product-item-name').find('a').text.strip()

        price_container = product_item.find('div', class_='price-box price-final_price')
        product_info['price_excluding_tax'] = price_container.find('span', class_='price-excluding-tax').find('span', class_='price').text.strip()
        product_info['price_including_tax'] = price_container.find('span', class_='price-including-tax').find('span', class_='price').text.strip()

        product_info['url'] = product_item.find('a', class_='product photo product-item-photo')['href']
        print(product_info)
        product_data.append(product_info)



    with open('./BeautifulSoup/products.yaml', 'w', encoding="utf-8") as yaml_file:
        yaml.dump(product_data, yaml_file, default_flow_style=False)
