from .prediction_model import PredictionModel
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input

class LSTMModel(PredictionModel):
    def __init__(self, input_shape):
        self.model = Sequential(
            [
                Input(
                    shape=input_shape
                ),  # Definieer de input shape hier met een Input laag
                LSTM(50, return_sequences=True),
                LSTM(50),
                Dense(1),
            ]
        )
        self.model.compile(optimizer="adam", loss="mean_squared_error")

    def train(self, X, y, epochs=100, batch_size=32):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)

    def predict(self, X):
        return self.model.predict(X)
