from flask import Blueprint
api_bp = Blueprint("api", __name__)

# Voeg routes toe
from . import routes
