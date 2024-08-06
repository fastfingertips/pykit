import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
import json
import os
from datetime import datetime

# Directory paths for saving JSON and image files
json_folder_path = "./generated/json/"
images_folder_path = "./generated/images/"
# URL to scrape
url = "https://www.camelcodes.net/books/"

def create_folder_if_not_exists(folder_path, verbose=False):
    """
    Create a folder if it does not exist.
    
    Parameters:
    folder_path (str): Path to the folder to be created.
    verbose (bool, optional): If True, print status messages. Defaults to False.
    """
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            if verbose:
                print(f"Created directory: {folder_path}")
        except Exception as e:
            if verbose:
                print(f"Failed to create directory {folder_path}: {e}")
            raise

def save_json_file(data, file_path='data.json', indent=4, verbose=False):
    """
    Save the scraped data to a JSON file.
    
    Parameters:
    data (dict): Data to be saved.
    file_path (str, optional): Path to the JSON file, including the file name. Defaults to 'data.json'.
    indent (int, optional): Indentation level for the JSON file. Defaults to 4.
    verbose (bool, optional): If True, print status messages. Defaults to False.
    """
    # Check if the directory of the provided file path exists and create it if necessary
    folder_path = os.path.dirname(file_path)
    
    if folder_path:
        create_folder_if_not_exists(folder_path, verbose)

    # Write the JSON data to the file
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=indent)
            if verbose:
                print(f"Data successfully saved to {file_path}")
    except Exception as e:
        if verbose:
            print(f"Failed to save data to {file_path}: {e}")
        raise



def fetch_and_resize_image(image_url):
    """Fetch an image from a URL, resize it, and save it locally."""
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image.thumbnail((400, 300))

    file_name = os.path.basename(image_url)
    file_path = os.path.join(images_folder_path, file_name)
    image.save(file_path, format="jpeg")
    return file_name


def main():
    """Main function to scrape book data and save it."""
    start_time = time.time()

    # Create necessary folders
    create_folder_if_not_exists(json_folder_path)
    create_folder_if_not_exists(images_folder_path)

    # Fetch HTML content from the URL
    print(f'Downloading html page: {url} ...')
    response = requests.get(url)
    html = response.content

    # Parse HTML using BeautifulSoup
    print('Parsing HTML file ...')
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.find_all('div', class_='kg-product-card-container')

    # List to store scraped book data
    scraped_data = []

    # Iterate over each book and extract data
    for book in books:
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

        print(f'Fetching and resizing image {os.path.basename(original_image_url)} ...')
        thumbnail = fetch_and_resize_image(original_image_url)

        # Append book data to the list
        scraped_data.append({
            'title': title,
            'rating': rating,
            'description': description,
            'original_image_url': original_image_url,
            'thumbnail_image': thumbnail,
            'buy_link': buy_link,
            'last_update_date': datetime.now().isoformat()
        })

    # Save scraped data to JSON
    print('Writing JSON file ...')
    save_json_file(scraped_data)

    # Calculate and print elapsed time
    elapsed_time = time.time() - start_time
    print(f"Took: {elapsed_time:.2f} seconds")


if __name__ == '__main__':
    print('Booting up...')
    main()
