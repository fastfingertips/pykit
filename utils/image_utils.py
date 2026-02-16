from pathlib import Path
import requests
from PIL import Image
from io import BytesIO

def fetch_image_content(url):
    """Fetches raw image content from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def process_and_save_image(image_content, save_path, thumbnail_size=(400, 300)):
    """Resizes an image from raw content and saves it to a path."""
    path = Path(save_path)
    image = Image.open(BytesIO(image_content))
    image.thumbnail(thumbnail_size)
    
    # Ensure it saves as JPEG and handle RGB conversion
    image.convert("RGB").save(path, format="JPEG")
    return path.name
