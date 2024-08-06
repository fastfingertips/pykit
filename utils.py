import os
import json

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
