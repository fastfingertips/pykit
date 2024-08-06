import os
import json

def save_json_file(data, file_path):
    """
    Save data to a JSON file.
    
    Parameters:
    data (dict): Data to be saved.
    file_path (str): Path to the JSON file.
    """
    create_folder_if_not_exists(os.path.dirname(file_path))
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to JSON file {file_path}")

def create_folder_if_not_exists(folder_path):
    """
    Create a folder if it does not exist.
    
    Parameters:
    folder_path (str): Path to the folder.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_file_path(*paths):
    """
    Combine paths into a single file path.
    
    Parameters:
    *paths (str): Paths to be combined.
    
    Returns:
    str: Combined file path.
    """
    return os.path.join(*paths)

def get_directory_path(file_path):
    """
    Get the directory path from a file path.
    
    Parameters:
    file_path (str): The file path.
    
    Returns:
    str: The directory path.
    """
    return os.path.dirname(file_path)
