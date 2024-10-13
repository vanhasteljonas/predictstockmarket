import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class DataPreprocessor:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_data(self, stock_symbol):
        # Data laden
        json_url = os.path.join(self.data_path, f"{stock_symbol}_historical.json")
        df = pd.read_json(json_url)
        return df

    def prepare_features(self, df, target_column):
        # Feature engineering en preprocessing stappen
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Bijvoorbeeld, standaardiseren van de features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        return X_scaled, y

    def train_test_split(self, X, y, test_size=0.2, random_state=42):
        # Train en test set splitsen
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        return X_train, X_test, y_train, y_test
