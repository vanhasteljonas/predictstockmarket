import pandas as pd
import os


class DataManager:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def download_data(self, url, subfolder, filename):
        """Download data van een URL en sla het op als een CSV bestand."""
        df = pd.read_csv(url)
        filepath = os.path.join(self.base_directory, subfolder, filename)
        df.to_csv(filepath, index=False)
        return filepath

    def load_data(self, filepath):
        """Laad data van een bestand."""
        return pd.read_csv(filepath)

    def save_data(self, df, filepath):
        """Sla een DataFrame op als een CSV bestand."""
        full_path = os.path.join(self.base_directory, filepath)
        df.to_csv(full_path, index=False)
        return full_path
