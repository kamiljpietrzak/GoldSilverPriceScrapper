import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize empty lists to store the scraped data
coin_names = []
coin_prices = []

# Start from the first page
page_number = 1

while True:
    # Form the URL of the page to scrape
    url = f"https://sklep.szlachetneinwestycje.pl/produkty/kategoria/srebro/srebrne-monety-bulionowe/page/{page_number}/"

    # Fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements containing coin names
    name_elements = soup.find_all('p', {'style': 'color: #273a4f;\n\t\tline-height: 1;', 'class': 'woocommerce-loop-product__title'})

    # Find all elements containing coin prices
    price_elements = soup.find_all('bdi')

    # If there are no more products, break the loop
    if not name_elements:
        break

    # Extract the text from these elements and store it in the lists
    for name_element in name_elements:
        coin_names.append(name_element.get_text().strip())

    for price_element in price_elements:
        coin_prices.append(price_element.get_text().strip().replace('\xa0', ' '))

    # Check if there is a next page
    next_page = soup.find('a', {'class': 'next page-numbers'})
    if next_page:
        page_number += 1
    else:
        break

# Create a DataFrame to display the scraped data in a table
df = pd.DataFrame({
    'Coin Name': coin_names,
    'Price': coin_prices
})
print(df)

# Save to CSV or any other processing
df.to_csv('scraped_coins.csv', index=False)
