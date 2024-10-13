from flask import Flask, send_from_directory
from flask_cors import CORS
from .api import api_bp
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

def create_app():
    app = Flask(__name__, static_folder="../../frontend/build")

    # Bepaal de omgeving en laad de juiste configuratie
    env = os.getenv("FLASK_ENV", "production")
    if env == "development":
        app.config.from_object(DevelopmentConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Configureer CORS op basis van de omgeving
    if app.config["DEBUG"]:
        CORS(app, resources={r"/api/*": {"origins": "*"}})  # Voor ontwikkeling
    else:
        CORS(
            app, resources={r"/api/*": {"origins": "https://marketinsighthub.com"}}
        )  # Voor productie

    # Registreer de blueprint met de url_prefix '/api'
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        # Als het pad niet begint met 'api/', serveer de index.html
        if not path.startswith("api/"):
            return send_from_directory(app.static_folder, path or "index.html")
        # Laat Flask het verzoek afhandelen als het een API-verzoek is
        # Flask zal automatisch een 404 geven als geen route matcht

    return app
