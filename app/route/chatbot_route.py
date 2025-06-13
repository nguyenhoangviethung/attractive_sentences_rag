from flask import Blueprint, request, jsonify
from chatbot.build_index import build_index
from chatbot.chatbot import query_rag,init_chatbot
from config import load_config
from chatbot import drive_utils as du
service = du.authenticate()

CONFIG = load_config()
FOLDER_ID = CONFIG["FOLDER_ID"]
chatbot_bp = Blueprint("chatbot_bp", __name__,url_prefix = "/chatbot")

mapping, index, embedder = init_chatbot(service = service, FOLDER_ID = FOLDER_ID)

@chatbot_bp.put('/build-index')
def build_index_r():
    res, status = build_index(FOLDER_ID = FOLDER_ID)
    return res, status

@chatbot_bp.post('/query-rag')
def query():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    data["mapping"] = mapping
    data["index"] = index
    data["embedder"] = embedder
    res, status = query_rag(data)
    return res, status

