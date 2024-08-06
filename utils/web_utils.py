import requests
from bs4 import BeautifulSoup

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
