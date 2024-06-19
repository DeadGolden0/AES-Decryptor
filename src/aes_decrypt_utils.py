from pathlib import Path
import requests

class FileDecryptorUtils:
    def __init__(self):
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / "gui" / "assets"

    def get_image(self, relative_path: str) -> Path:
        return self.assets_path / relative_path
    
    def check_for_updates(self, current_version):
        try:
            response = requests.get('https://api.github.com/repos/DeadGolden0/AES-Decryptor/tags')
            response.raise_for_status()
            tags = response.json()
            latest_version = tags[0]['name'] if tags else current_version

            if latest_version > current_version:
                return True, latest_version
            return False, latest_version
        except requests.RequestException as e:
            print(f"Failed to check for updates: {e}")
            return False, current_version
