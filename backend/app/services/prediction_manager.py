from ..models.prediction_model import PredictionModel
from ..models.xgboost_model import XGBoostModel
from ..models.lstm_model import LSTMModel
import os
import joblib
import pandas as pd
from datetime import datetime, timedelta


class PredictionManager:

    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path
        self.models = {
            "xgboost": XGBoostModel(),
            "lstm": LSTMModel(input_shape=(1, 1)),
        }

    def train_and_save_model(self, stock_symbol, model_name):
        # Instantieer DataPreprocessor met het pad naar de data
        data_preprocessor = DataPreprocessor(self.data_path)

        # Laden en voorbereiden van de data voor training
        df = data_preprocessor.load_data(stock_symbol)
        X, y = data_preprocessor.prepare_features(df, target_column="Price")

        # Opsplitsen van de data in train- en testsets
        X_train, X_test, y_train, y_test = data_preprocessor.train_test_split(X, y)

        # Trainen van het model
        if model_name in self.models:
            self.models[model_name].train(X_train, y_train)

            # Opslaan van het getrainde model
            model_filename = f"{model_name}_{stock_symbol}.pkl"
            joblib.dump(
                self.models[model_name], os.path.join(self.model_path, model_filename)
            )
        else:
            raise ValueError(f"Model {model_name} is not supported.")

    def load_model(self, stock_symbol, model_name):
        # Laden van een eerder getraind en opgeslagen model
        model_filename = f"{model_name}_{stock_symbol}.pkl"
        if os.path.exists(os.path.join(self.model_path, model_filename)):
            return joblib.load(os.path.join(self.model_path, model_filename))
        else:
            raise FileNotFoundError(
                f"The model {model_name} for {stock_symbol} is not trained yet."
            )

    def predict_with_model(self, stock_symbol, duration, model_name):
        # Laden van het getrainde model
        model = self.load_model(stock_symbol, model_name)

        # Laden en voorbereiden van de voorspellingsdata
        df = pd.read_json(
            os.path.join(self.data_path, f"{stock_symbol}_prediction.json")
        )
        # Filter de data tot de einddatum zoals eerder gedefinieerd
        # ...

        # Selecteren van de kolommen die nodig zijn voor de voorspelling
        # ...

        # Voer de voorspelling uit met het geladen model
        predictions = model.predict(features)
        return predictions
