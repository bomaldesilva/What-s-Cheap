import requests
import json
import sys

sys.path.insert(0, 'bs4.zip')
from bs4 import BeautifulSoup

# Imitate the Mozilla browser.
headers = {'User-Agent': 'Mozilla/5.0'}

product_laughs="https://scrape-sm1.github.io/site1/COCONUT%20market1super.html"
product_glomark="https://glomark.lk/coconut/p/11624"

def compare_prices(product_laughs, product_glomark):
    # Request for Laughs supermarket`
    response_laughs = requests.get(product_laughs, headers=headers)
    # Parse the HTML response using BeautifulSoup
    soup_laughs = BeautifulSoup(response_laughs.text, 'html.parser')

    # Extract the price and product name from Laughs
    price_laughs = soup_laughs.find('span', {'class': 'regular-price'}).text.strip()
    product_name_laughs = soup_laughs.find('h1').text.strip()  # Ensure you are targeting the correct element

    # Request for Glomark supermarke
    response_glomark = requests.get(product_glomark, headers=headers)
    # Parse the HTML response to find the JSON data
    soup_glomark = BeautifulSoup(response_glomark.text, 'html.parser')
    script_glomark = soup_glomark.find('script', {'type': 'application/ld+json'})


    # Check if script_glomark is not None
    if script_glomark is not None:
        # Load the JSON data from the script content
        data_glomark = json.loads(script_glomark.string)  # Use .string or .text to get the JSON string

        # Extract the price and product name from Glomark
        price_glomark = data_glomark['offers'][0]['price']
        product_name_glomark = data_glomark['name']

        # Parse the prices as floats
        price_laughs = float(price_laughs.replace("Rs.", "").replace(",", "").strip())
        price_glomark = float(price_glomark)

        # Print product details
        print('Laughs  ', product_name_laughs, 'Rs.: ', price_laughs)
        print('Glomark ', product_name_glomark, 'Rs.: ', price_glomark)

        # Compare prices and recommend the cheaper option
        if price_laughs > price_glomark:
            print('Glomark is cheaper Rs.:', price_laughs - price_glomark)
        elif price_laughs < price_glomark:
            print('Laughs is cheaper Rs.:', price_glomark - price_laughs)
        else:
            print('Price is the same.')
    else:
        print("No JSON data found in Glomark's response.")

compare_prices(product_laughs,product_glomark)
