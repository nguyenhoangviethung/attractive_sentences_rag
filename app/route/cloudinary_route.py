from flask import Blueprint, request, jsonify
from service import cloudinary_service as cs
cloudinary_bp = Blueprint("cloudinary_bp", __name__,url_prefix = "/cloudinary")

@cloudinary_bp.route('/')
def index():
    return "Heloo cloudinary"

@cloudinary_bp.post('/upload-image')
def upload_image():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    res, status = cs.upload_image(data)
    return res, status