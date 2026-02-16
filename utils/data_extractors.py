def get_text_or_default(tag, default=''):
    """Extract text from a BeautifulSoup tag or return default."""
    return tag.text.strip() if tag else default

def get_image_url(image_tag):
    """Extract the image URL from an image tag."""
    return image_tag['src'] if image_tag and 'src' in image_tag.attrs else ''

def get_link(link_tag):
    """Extract the link URL from a link tag."""
    return link_tag['href'] if link_tag else ''

def extract_book_raw_data(book_container):
    """
    Extracts raw strings from a book HTML container.
    Returns a dictionary of extracted data.
    """
    title_tag = book_container.find('h4', class_='kg-product-card-title')
    rating_stars = book_container.find_all('span', class_='kg-product-card-rating-star')
    rating_stars_active = book_container.find_all('span', class_='kg-product-card-rating-active')
    description_tag = book_container.find('div', class_='kg-product-card-description')
    image_tag = book_container.find('img', class_='kg-product-card-image')
    buy_link_tag = book_container.find('a', class_='kg-product-card-button', href=True)

    return {
        'title': get_text_or_default(title_tag, 'No Title'),
        'rating': f"{len(rating_stars_active)}/{len(rating_stars)}",
        'description': get_text_or_default(description_tag, 'No Description'),
        'image_url': get_image_url(image_tag),
        'buy_link': get_link(buy_link_tag)
    }
