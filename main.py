from config import JSON_FOLDER_PATH, IMAGES_FOLDER_PATH, URL
from utils.file_utils import save_json_file, create_folder_if_not_exists, get_file_path
from utils.web_utils import fetch_html_content
from utils.data_extractors import extract_book_data
from utils.timing_utils import Timer


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
    with Timer():
        # Create necessary folders
        create_folder_if_not_exists(JSON_FOLDER_PATH)
        create_folder_if_not_exists(IMAGES_FOLDER_PATH)

        # Scrape books data
        print(f'Downloading html page: {URL} ...')
        scraped_data = scrape_books(URL, IMAGES_FOLDER_PATH)

        # Save scraped data to JSON
        json_file_path = get_file_path(JSON_FOLDER_PATH, 'books.json')
        print('Writing JSON file ...')
        save_json_file(scraped_data, file_path=json_file_path)

if __name__ == '__main__':
    print('Booting up...')
    main()
