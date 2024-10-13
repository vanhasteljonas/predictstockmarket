from abc import ABC, abstractmethod


class PredictionModel(ABC):

    @abstractmethod
    def train(self, X, y):
        """
        Train het model met de gegeven data.
        X: Feature matrix
        y: Target vector
        """
        pass

    @abstractmethod
    def predict(self, X):
        """
        Voer een voorspelling uit met het model.
        X: Feature matrix voor het maken van voorspellingen
        """
        pass
