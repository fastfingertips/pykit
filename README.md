# Web Scraping JSON Data and Images from HTML: Python Tutorial 📖

This repository contains a Python-based project demonstrating web scraping techniques to extract book data and images from a website. The project is inspired by the tutorial “Web Scraping JSON Data and Images from HTML: Python Tutorial 📖” by Moulaye Eli, published on CamelCodes.net.

## 📚 Overview

This project focuses on:
- Extracting book details and images from the [CamelCodes Books Page](https://www.camelcodes.net/books/).
- Structuring the extracted data into a JSON format.
- Processing and saving images as thumbnails.

The aim is to provide a comprehensive guide to web scraping, including handling both textual and visual data.

## 🔧 Prerequisites

To run this project, ensure that Python 3 is installed on your system. Additionally, you will need to install the following Python libraries:

- `beautifulsoup4` for parsing HTML content.
- `pillow` for image processing.
- `requests` for making HTTP requests.

Create a `requirements.txt` file with the following content:

```plaintext
beautifulsoup4==4.12.3
pillow==10.2.0
requests==2.31.0
```

Install the dependencies using the following command:

```bash
python3 -m pip install -r requirements.txt
```

## 🛠️ Project Structure

- **`file_utils.py`**: Contains utility functions for file operations such as creating directories and saving JSON files.
- **`image_utils.py`**: Includes functions for downloading, resizing, and saving images.
- **`web_utils.py`**: Manages web requests and HTML content retrieval.
- **`data_extractors.py`**: Extracts and processes book information from HTML content.
- **`timing_utils.py`**: Provides timing utilities to measure script execution duration.
- **`main.py`**: Orchestrates the web scraping process, including data extraction and image processing.

## 🚀 Usage

1. **Setup**: Ensure the necessary folders for JSON and image storage are created by the script.
2. **Execution**: The script will fetch HTML content from the target URL, extract book details, and process images.
3. **Output**: The extracted data will be saved in a JSON file, and images will be resized and stored in the designated folder.

To execute the script, run:

```bash
python3 main.py
```

## 🖥️ Example Output

Upon successful execution, you will find:
- A `books.json` file containing the structured book data.
- Resized images saved in the specified directory.

## 📜 Acknowledgements

This project is inspired by the tutorial [Web Scraping JSON Data and Images from HTML: Python Tutorial 📖](https://camelcodes.net/web-scraping-python-beautifulsoup-image-processing-html) by Moulaye Eli.