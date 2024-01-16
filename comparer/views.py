# comparer/views.py
from django.shortcuts import render
from .forms import SearchForm
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode


def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']

            # Perform web scraping on Amazon
            amazon_data = get_amazon_product_info(product_name)

            # Perform web scraping on Flipkart
            flipkart_data = get_flipkart_product_info(product_name)

            # Pass the scraped data to the template
            return render(request, 'search_results.html', {'amazon_data': amazon_data, 'flipkart_data': flipkart_data})

    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})

def get_amazon_product_info(product_name):
    base_url = "https://www.amazon.in/s"
    params = {"k": product_name}
    search_url = f"{base_url}?{urlencode(params)}"

    response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product name and price from the product page
        name_element = soup.find('span', {'id': 'productTitle'})
        name = name_element.text.strip() if name_element else "N/A"

        price_element = soup.find('span', {'class': 'a-price-whole'})
        price = price_element.text.strip() if price_element else "N/A"

        # Print the price
        # print("\nPrice:", price)

        return {'name': product_name, 'price': price}

    else:
        print(f"Error: {response.status_code}")
        return {'name': 'N/A', 'price': 'N/A'}
# def scrape_amazon(product_name):
#     amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'

#     response = requests.get(amazon_url)
#     soup = BeautifulSoup(response.text, 'lxml')

#     # Extract relevant information
#     name_element = soup.select_one('.s-title-instructions a span')
#     name = name_element.text.strip() if name_element else 'Not available'

#     price_element = soup.select_one('.a-offscreen')
#     price = price_element.text.strip() if price_element else 'Not available'

#     # Add more data points as needed

#     return {'name': name, 'price': price}

def get_flipkart_product_info(product_name):
    base_url = "https://www.flipkart.com/search"
    params = {"q": product_name}
    search_url = f"{base_url}?{urlencode(params)}"

    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract price from the product page
        price_element = soup.find('div', {'class': '_30jeq3'})
        price = price_element.text.strip() if price_element else "N/A"

        # Print the price
        # print("\nPrice:", price)

        return {'name': product_name, 'price': price}

    else:
        # print(f"Error: {response.status_code}")
        return {'name': product_name, 'price': 'N/A'}
# def scrape_flipkart(product_name):
#     flipkart_url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "%20")}'

#     response = requests.get(flipkart_url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Extract relevant information
#     name_element = soup.select_one('._30jeq3._16Jk6d')
#     name = name_element.text.strip() if name_element else 'Not available'

#     price_element = soup.select_one('._1vC4OE._2rQ-NK')
#     price = price_element.text.strip() if price_element else 'Not available'

#     # Add more data points as needed

#     return {'name': name, 'price': price}
