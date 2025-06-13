from flask import request, jsonify, Blueprint

from database.model import SentenceData

from service import mongoDB_service as ms

mongoDB_bp = Blueprint("mongoDB_bp",__name__, url_prefix = "/sentence")

@mongoDB_bp.route('/')
def index():
    return "Hello world"

@mongoDB_bp.post('/add-sentence')
def add_sentence():
    data = request.json
    res, status = ms.add_sentence(data)
    return res, status
        

@mongoDB_bp.get('/sentences')
def get_sentences():
    res, status = ms.get_sentences()
    return res, status

@mongoDB_bp.get('/pre-data')
def pre_data():
    res, status = ms.pre_data()
    return res, status

@mongoDB_bp.get("/pending")
def pending():
    res, status = ms.get_temp_sentences()
    return res, status

@mongoDB_bp.post('/approve')
def approve():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    res, status = ms.approve_text(data)
    return res, status
@mongoDB_bp.post('/deny')
def deny():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    res, status = ms.delete_temp_sentence(data)
    return res, status