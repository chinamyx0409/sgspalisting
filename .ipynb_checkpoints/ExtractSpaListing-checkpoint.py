import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize empty lists for data
spa_names = []
dates = []
shop_images = []
staff_images_list = []
descriptions = []
service_descriptions = []
contact_infos = []
whatsapp_links = []

# URL of the page to scrape
url = 'https://g1298.com/category/west-area/'

# Send a request to the website
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all articles in the West Area category
articles = soup.find_all('article', class_='category-west-area')

# Loop through each article and extract information
for article in articles:
    # Extract the spa name
    spa_name = article.find('h2', class_='entry-title').get_text()
    spa_names.append(spa_name)

    # Extract the date
    date = article.find('time', class_='entry-date').get_text()
    dates.append(date)

    # Extract the shop image source and dimensions
    shop_image_tag = article.find('div', class_='post-thumbnail').find('img')
    if shop_image_tag and 'data-src' in shop_image_tag.attrs:
        shop_image_src = shop_image_tag['data-src']
        shop_image_width = shop_image_tag['data-width']
        shop_image_height = shop_image_tag['data-height']
    else:
        shop_image_src = None
        shop_image_width = None
        shop_image_height = None
    shop_images.append((shop_image_src, shop_image_width, shop_image_height))

    # Extract all staff images
    staff_images = article.find_all('figure', class_='wp-block-image')
    staff_info = []
    for img in staff_images:
        img_tag = img.find('img')
        if img_tag and 'data-src' in img_tag.attrs:
            staff_image_src = img_tag['data-src']
            staff_image_width = img_tag['data-width']
            staff_image_height = img_tag['data-height']
            staff_image_alt = img_tag['alt']
            staff_info.append({
                'source': staff_image_src,
                'width': staff_image_width,
                'height': staff_image_height,
                'alt': staff_image_alt
            })
    staff_images_list.append(staff_info)

    # Extract the shop description
    description = article.find('h2', class_='wp-block-heading').get_text()
    descriptions.append(description)

    # Extract the service description
    service_description = article.find('p', class_='has-text-align-center').get_text()
    service_descriptions.append(service_description)

    # Extract contact and WhatsApp information
    contact_info = service_description
    whatsapp_image = article.find('img', alt=True, src=True)
    whatsapp_link = whatsapp_image['src'] if whatsapp_image and 'data-src' in whatsapp_image.attrs else None
    contact_infos.append(contact_info)
    whatsapp_links.append(whatsapp_link)

# Create a Pandas DataFrame
data = {
    'Spa Name': spa_names,
    'Date': dates,
    'Shop Image': shop_images,
    'Staff Images': staff_images_list,
    'Description': descriptions,
    'Services': service_descriptions,
    'Contact': contact_infos,
    'WhatsApp Link': whatsapp_links
}

df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
excel_file = 'spa_data.xlsx'
df.to_excel(excel_file, index=False)

# Print the path to the saved Excel file
print(f"DataFrame saved to {excel_file}")
