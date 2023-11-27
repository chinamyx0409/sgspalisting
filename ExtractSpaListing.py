import re
import requests
from bs4 import BeautifulSoup
from time import sleep

# URL of the page to scrape (can be made dynamic for different categories)
url = 'https://g1298.com/category/central-area/'

# Headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to clean the services description
def clean_services(services, words_to_remove):
    cleaned_services = []
    for service in services:
        for word in words_to_remove:
            service = re.sub(r'\b{}\b'.format(re.escape(word)), '', service, flags=re.IGNORECASE)
        cleaned_services.append(service.strip())
    return ', '.join(cleaned_services).replace(' ,', ',').strip()

# Function to scrape a single page
def scrape_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

# Main scraping function
def main():
    # Initialize a list to store extracted data
    extracted_data = []

    # Scrape the first page (can be extended to scrape multiple pages)
    soup = scrape_page(url)
    if soup:
        articles = soup.find_all('article', class_='category-central-area')
        for article in articles:
            try:
                data = {}
                data['spa_name'] = article.find('h2', class_='entry-title').get_text().strip()
                # Add other data extractions here...
                # For example, data['date'] = article.find('time', class_='entry-date').get_text().strip()

                extracted_data.append(data)

            except Exception as e:
                print(f"An error occurred while processing an article: {e}")

    # Output or store the extracted data
    for data in extracted_data:
        print(data)

    # Delay for respectful scraping
    sleep(1)

if __name__ == '__main__':
    main()
