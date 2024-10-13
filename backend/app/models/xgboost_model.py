from .prediction_model import PredictionModel
from xgboost import XGBRegressor

class XGBoostModel(PredictionModel):

    def __init__(self, n_estimators=100, max_depth=3, learning_rate=0.1):
        self.model = XGBRegressor(
            n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate
        )

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
