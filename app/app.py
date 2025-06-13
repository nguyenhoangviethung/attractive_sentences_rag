from flask import Flask, request, jsonify
from flask_cors import CORS
from database import connect_db, connect_cloudinary
from database.model import SentenceData

def create_app(CONFIG):
    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    db = connect_db(CONFIG)
    connect_cloudinary(CONFIG)
    from app.route import register_routes
    register_routes(app)
    return app
