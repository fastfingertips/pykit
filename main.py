import time
import os
from datetime import datetime
from config import JSON_FOLDER_PATH, IMAGES_FOLDER_PATH, URL
from utils.file_utils import save_json_file, create_folder_if_not_exists
from utils.image_utils import fetch_and_resize_image
from utils.web_utils import fetch_html_content

def get_text_or_default(tag, default=''):
    """
    Extract text from a BeautifulSoup tag or return a default value if tag is None.

    Parameters:
    tag (BeautifulSoup tag): The tag to extract text from.
    default (str): Default value to return if tag is None.

    Returns:
    str: Extracted text or default value.
    """
    return tag.text.strip() if tag else default

def get_image_url(image_tag):
    """
    Extract the image URL from a BeautifulSoup image tag.

    Parameters:
    image_tag (BeautifulSoup tag): The tag to extract the image URL from.

    Returns:
    str: Image URL or an empty string if the URL is not found.
    """
    return image_tag['src'] if image_tag and 'src' in image_tag.attrs else ''

def get_link(link_tag):
    """
    Extract the link URL from a BeautifulSoup link tag.

    Parameters:
    link_tag (BeautifulSoup tag): The tag to extract the link URL from.

    Returns:
    str: Link URL or an empty string if the link is not found.
    """
    return link_tag['href'] if link_tag else ''

def extract_book_data(book, images_folder_path):
    """
    Extract data from a single book entry.

    Parameters:
    book (BeautifulSoup tag): A BeautifulSoup tag representing a book entry.
    images_folder_path (str): Path to the folder where images will be saved.

    Returns:
    dict: Extracted data for the book.
    """
    title_tag = book.find('h4', class_='kg-product-card-title')
    rating_stars = book.find_all('span', class_='kg-product-card-rating-star')
    rating_stars_active = book.find_all('span', class_='kg-product-card-rating-active')
    description_tag = book.find('div', class_='kg-product-card-description')
    image_tag = book.find('img', class_='kg-product-card-image')
    buy_link_tag = book.find('a', class_='kg-product-card-button', href=True)

    title = get_text_or_default(title_tag, 'No Title')
    rating = f"{len(rating_stars_active)}/{len(rating_stars)}"
    description = get_text_or_default(description_tag, 'No Description')
    original_image_url = get_image_url(image_tag)
    buy_link = get_link(buy_link_tag)

    thumbnail = fetch_and_resize_image(original_image_url, images_folder_path)

    return {
        'title': title,
        'rating': rating,
        'description': description,
        'original_image_url': original_image_url,
        'thumbnail_image': thumbnail,
        'buy_link': buy_link,
        'last_update_date': datetime.now().isoformat()
    }

def scrape_books(url, images_folder_path):
    """
    Scrape book data from the given URL.
    
    Parameters:
    url (str): The URL to scrape book data from.
    images_folder_path (str): Path to the folder where images will be saved.
    
    Returns:
    list: A list of dictionaries containing scraped book data.
    """
    soup = fetch_html_content(url)
    books = soup.find_all('div', class_='kg-product-card-container')
    return [extract_book_data(book, images_folder_path) for book in books]

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
    scraped_data = scrape_books(URL, IMAGES_FOLDER_PATH)

    # Save scraped data to JSON
    print('Writing JSON file ...')
    save_json_file(scraped_data, file_path=os.path.join(JSON_FOLDER_PATH, 'books.json'))

    # Calculate and print elapsed time
    elapsed_time = time.time() - start_time
    print(f"Took: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    print('Booting up...')
    main()
