from flask import Blueprint, request, jsonify
from chatbot.build_index import build_index
from chatbot.chatbot import query_rag,init_chatbot
import os
from dotenv import load_dotenv
from chatbot import drive_utils as du
service = du.authenticate()

load_dotenv()
FOLDER_ID =os.getenv("FOLDER_ID")
chatbot_bp = Blueprint("chatbot_bp", __name__,url_prefix = "/chatbot")

mapping, index, embedder = init_chatbot(service = service, folder_id = FOLDER_ID)

@chatbot_bp.put('/build_index')
def build_index_r():
    res, status = build_index(FOLDER_ID = FOLDER_ID)
    return res, status

@chatbot_bp.get('/query_rag')
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

