import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
import os
from datetime import datetime
from utils import save_json_file, create_folder_if_not_exists

# Directory paths for saving JSON and image files
JSON_FOLDER_PATH = "./generated/json/"
IMAGES_FOLDER_PATH = "./generated/images/"
# URL to scrape
URL = "https://www.camelcodes.net/books/"

def fetch_and_resize_image(image_url):
    """
    Fetch an image from a URL, resize it, and save it locally.
    
    Parameters:
    image_url (str): URL of the image to fetch and resize.
    
    Returns:
    str: The filename of the saved image.
    """
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image.thumbnail((400, 300))

    file_name = os.path.basename(image_url)
    file_path = os.path.join(IMAGES_FOLDER_PATH, file_name)
    image.save(file_path, format="jpeg")
    return file_name

def fetch_html_content(url):
    """
    Fetch the HTML content of a given URL.
    
    Parameters:
    url (str): The URL to fetch the HTML content from.
    
    Returns:
    BeautifulSoup: Parsed HTML content.
    """
    response = requests.get(url)
    html = response.content
    return BeautifulSoup(html, 'html.parser')

def extract_book_data(book):
    """
    Extract data from a single book entry.
    
    Parameters:
    book (BeautifulSoup tag): A BeautifulSoup tag representing a book entry.
    
    Returns:
    dict: Extracted data for the book.
    """
    title_tag = book.find('h4', class_='kg-product-card-title')
    title = title_tag.text.strip() if title_tag else 'No Title'

    rating_stars = book.find_all('span', class_='kg-product-card-rating-star')
    rating_stars_active = book.find_all('span', class_='kg-product-card-rating-active')
    rating = f"{len(rating_stars_active)}/{len(rating_stars)}"

    description_tag = book.find('div', class_='kg-product-card-description')
    description = description_tag.text.strip() if description_tag else 'No Description'

    image_tag = book.find('img', class_='kg-product-card-image')
    original_image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else ''

    buy_link_tag = book.find('a', class_='kg-product-card-button', href=True)
    buy_link = buy_link_tag['href'] if buy_link_tag else ''

    thumbnail = fetch_and_resize_image(original_image_url)

    return {
        'title': title,
        'rating': rating,
        'description': description,
        'original_image_url': original_image_url,
        'thumbnail_image': thumbnail,
        'buy_link': buy_link,
        'last_update_date': datetime.now().isoformat()
    }

def scrape_books(url):
    """
    Scrape book data from the given URL.
    
    Parameters:
    url (str): The URL to scrape book data from.
    
    Returns:
    list: A list of dictionaries containing scraped book data.
    """
    soup = fetch_html_content(url)
    books = soup.find_all('div', class_='kg-product-card-container')
    return [extract_book_data(book) for book in books]

def main():
    """
    Main function to scrape book data and save it.
    """
    start_time = time.time()

    # Create necessary folders
    create_folder_if_not_exists(JSON_FOLDER_PATH)
    create_folder_if_not_exists(IMAGES_FOLDER_PATH)

    # Scrape books data
    print(f'Downloading html page: {URL} ...')
    scraped_data = scrape_books(URL)

    # Save scraped data to JSON
    print('Writing JSON file ...')
    save_json_file(scraped_data, file_path=os.path.join(JSON_FOLDER_PATH, 'books.json'))

    # Calculate and print elapsed time
    elapsed_time = time.time() - start_time
    print(f"Took: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    print('Booting up...')
    main()
