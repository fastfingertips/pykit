from pathlib import Path
from config import JSON_FOLDER_PATH, IMAGES_FOLDER_PATH, URL
from utils.file_utils import save_json_file, create_folder_if_not_exists, get_file_path
from utils.web_utils import fetch_html_content
from utils.data_extractors import extract_book_raw_data
from utils.image_utils import fetch_image_content, process_and_save_image
from utils.timing_utils import Timer
from models.book import Book

class BookScraper:
    def __init__(self, url=URL, json_path=JSON_FOLDER_PATH, image_path=IMAGES_FOLDER_PATH):
        self.url = url
        self.json_path = json_path
        self.image_path = image_path
        self.books = []

    def _prepare_environment(self):
        """Creates necessary directories for storage."""
        create_folder_if_not_exists(self.json_path)
        create_folder_if_not_exists(self.image_path)

    def _process_book_image(self, image_url):
        """Downloads and processes a single book image."""
        if not image_url:
            return "no_image.jpg"
            
        try:
            content = fetch_image_content(image_url)
            filename = Path(image_url).name
            save_path = get_file_path(self.image_path, filename)
            return process_and_save_image(content, save_path)
        except Exception as e:
            print(f"Failed to process image {image_url}: {e}")
            return "error_image.jpg"

    def scrape(self):
        """Orchestrates the scraping and object creation process."""
        print(f'Downloading html page: {self.url} ...')
        soup = fetch_html_content(self.url)
        book_containers = soup.find_all('div', class_='kg-product-card-container')
        
        self.books = []
        for container in book_containers:
            # 1. Extract raw data (Pure parsing)
            raw_data = extract_book_raw_data(container)
            
            # 2. Process image (I/O Side Effect managed by Scraper)
            thumbnail_name = self._process_book_image(raw_data['image_url'])
            
            # 3. Create Book Model instance
            book = Book(
                title=raw_data['title'],
                rating=raw_data['rating'],
                description=raw_data['description'],
                original_image_url=raw_data['image_url'],
                thumbnail_image=thumbnail_name,
                buy_link=raw_data['buy_link']
            )
            self.books.append(book)
            
        return self.books

    def save(self, filename='books.json'):
        """Saves the scraped data to a JSON file."""
        if not self.books:
            print("No data to save. Run scrape() first.")
            return

        scraped_data = [book.to_dict() for book in self.books]
        full_path = get_file_path(self.json_path, filename)
        
        print(f'Writing JSON file to {full_path} ...')
        save_json_file(scraped_data, file_path=full_path)

    def run(self):
        """Runs the full pipeline with timing."""
        try:
            with Timer():
                self._prepare_environment()
                self.scrape()
                self.save()
        except Exception as e:
            print(f"An error occurred during execution: {e}")

def main():
    scraper = BookScraper()
    scraper.run()

if __name__ == '__main__':
    print('Booting up...')
    main()
