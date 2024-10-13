from app import create_app
import os

config_type = os.getenv("FLASK_ENV", "development")

config_dict = {
    "development": "app.config.DevelopmentConfig",
    "testing": "app.config.TestingConfig",
    "production": "app.config.ProductionConfig",
}

app = create_app(config_dict.get(config_type.lower(), "app.config.DevelopmentConfig"))

if __name__ == "__main__":
    app.run()
