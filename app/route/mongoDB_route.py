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

@mongoDB_bp.route('/pre-data')
def pre_data():
    res, status = ms.pre_data()
    return res, status