from flask import request, jsonify, Blueprint
import os
import pandas as pd
from . import api_bp
from app.services.prediction_manager import PredictionManager
from ..services.data_manager import DataManager
from datetime import datetime, timedelta

# Defineer het pad naar je data en modellen
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "assets")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models")

data_manager = DataManager(DATA_PATH)

# Maak een instantie van de PredictionManager
prediction_manager = PredictionManager(DATA_PATH, MODEL_PATH)

from . import api_bp

# Gebruik de blueprint om de route te definiëren
@api_bp.route("/contact", methods=["POST"])
def contact():
    data = request.json
    # Verwerk de ingezonden contactgegevens
    return jsonify(status="success", data=data)  # status 200


@api_bp.route("/stocks", methods=["GET"])
def get_stocks():
    print("Accessing /stocks endpoint")  # Debugging statement
    stocks = ["AAPL", "GOOG", "MSFT", "AMZN", "FB"]
    return jsonify(stocks)


@api_bp.route("/stock_data", methods=["POST"])
def get_stock_data():
    data = request.json
    stock_symbol = data.get("stock")  # AAPL
    duration = data.get("duration")  # 1m

    # Construct the path to the JSON file
    json_url = os.path.join(
        os.path.dirname(__file__), "..", "assets", "AAPL_prediction.json"
    )

    # Load the JSON data into a pandas DataFrame
    df = pd.read_json(json_url)

    # Select only the 'Date', 'Open', and 'Rsi14' columns
    df_subset = df[["Date", "Open", "Rsi14"]]

    # Convert the selected columns of the DataFrame to a JSON-serializable format and return it
    return jsonify(status="success", data=df_subset.to_dict(orient="records"))


@api_bp.route("/stock_data_prediction", methods=["POST"])
def get_stock_data_prediction():
    data = request.json
    stock_symbol = data.get("stock")  # AAPL
    duration = data.get("duration")  # 1m
    model_name = data.get("model", "xgboost")  # Standaard naar 'xgboost' als

    # Voer de voorspelling uit via de PredictionManager
    try:
        predictions = prediction_manager.predict_model(
            stock_symbol,
            duration,
            model_name,
        )
        return jsonify(status="success", data=predictions)
    except ValueError as e:
        return jsonify(status="error", message=str(e)), 400


@api_bp.route("/train_model", methods=["POST"])
def train_model():
    data = request.json
    stock_symbol = data.get("stock")
    model_name = data.get("model", "xgboost")

    try:
        prediction_manager.train_and_save_model(stock_symbol, model_name)
        return jsonify(status="success", message="Model trained successfully")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400


def get_historical_data_url(ticker):
    unix_oldest_date = 0
    unix_newest_date = int(datetime.now().timestamp())
    return f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={unix_oldest_date}&period2={unix_newest_date}&interval=1d&events=history&includeAdjustedClose=true"


@api_bp.route("/download_and_save_data/<ticker>", methods=["GET"])
def download_and_save_data(ticker):
    url = get_historical_data_url(ticker)
    filename = f"{ticker}_historical.csv"
    subfolder = "historical"
    try:
        filepath = data_manager.download_data(url, subfolder, filename)
        return jsonify(
            status="success",
            message="Data downloaded and saved successfully",
            file_path=filepath,
        )
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500
