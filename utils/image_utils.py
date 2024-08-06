import requests
from PIL import Image
from io import BytesIO
import os

def fetch_and_resize_image(image_url, images_folder_path):
    """
    Fetch an image from a URL, resize it, and save it locally.

    Parameters:
    image_url (str): URL of the image to fetch and resize.
    images_folder_path (str): Path to the folder where images will be saved.

    Returns:
    str: The filename of the saved image.
    """
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image.thumbnail((400, 300))

    file_name = os.path.basename(image_url)
    file_path = os.path.join(images_folder_path, file_name)
    image.save(file_path, format="jpeg")
    return file_name
