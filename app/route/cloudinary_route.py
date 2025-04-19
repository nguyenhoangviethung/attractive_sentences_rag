from flask import Blueprint, request, jsonify

cloudinary_bp = Blueprint("cloudinary_bp", __name__,url_prefix = "/cloudinary")

@cloudinary_bp.route('/')
def index():
    return "Heloo cloudinary"