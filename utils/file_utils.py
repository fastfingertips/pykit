from pathlib import Path
import json

def save_json_file(data, file_path):
    """
    Save data to a JSON file.
    Expects the directory to already exist.
    """
    path = Path(file_path)
    with path.open('w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to JSON file {path}")

def create_folder_if_not_exists(folder_path):
    """Create a folder if it does not exist using pathlib."""
    Path(folder_path).mkdir(parents=True, exist_ok=True)

def get_file_path(directory, filename):
    """Combine directory and filename into a Path object."""
    return str(Path(directory) / filename)
