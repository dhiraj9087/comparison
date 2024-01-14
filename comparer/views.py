# comparer/views.py
from django.shortcuts import render
from .forms import SearchForm
import requests
from bs4 import BeautifulSoup

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']

            # Perform web scraping on Amazon
            amazon_data = scrape_amazon(product_name)

            # Perform web scraping on Flipkart
            flipkart_data = scrape_flipkart(product_name)

            # Pass the scraped data to the template
            return render(request, 'search_results.html', {'amazon_data': amazon_data, 'flipkart_data': flipkart_data})

    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})


def scrape_amazon(product_name):
    amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'

    response = requests.get(amazon_url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract relevant information
    name_element = soup.select_one('.s-title-instructions a span')
    name = name_element.text.strip() if name_element else 'Not available'

    price_element = soup.select_one('.a-offscreen')
    price = price_element.text.strip() if price_element else 'Not available'

    # Add more data points as needed

    return {'name': name, 'price': price}


def scrape_flipkart(product_name):
    flipkart_url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "%20")}'

    response = requests.get(flipkart_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract relevant information
    name_element = soup.select_one('._30jeq3._16Jk6d')
    name = name_element.text.strip() if name_element else 'Not available'

    price_element = soup.select_one('._1vC4OE._2rQ-NK')
    price = price_element.text.strip() if price_element else 'Not available'

    # Add more data points as needed

    return {'name': name, 'price': price}
