import os
from flask import jsonify
import time
import json
import faiss
from sentence_transformers import SentenceTransformer
from chatbot import drive_utils as du  
from config import load_config

CONFIG = load_config()

FOLDER_ID = CONFIG["FOLDER_ID"]
CACHE_EXPIRY_SECONDS = 7 * 24 * 3600  

def is_file_expired(file_path, expiry_seconds=CACHE_EXPIRY_SECONDS):
    if not os.path.exists(file_path):
        return True
    file_mtime = os.path.getmtime(file_path)
    now = time.time()
    age = now - file_mtime
    return age > expiry_seconds

def load_mapping_with_cache(service, FOLDER_ID, file_name="mapping.json"):
    if is_file_expired(file_name):
        print(f"[Cache] File {file_name} đã cũ hoặc không tồn tại, tải lại từ Drive...")
        file_id = du.find_file_id(service, FOLDER_ID, file_name)
        if not file_id:
            raise FileNotFoundError(f"Không tìm thấy {file_name} trong folder {FOLDER_ID}")
        du.download_file(service, file_id, file_name)  
    else:
        print(f"[Cache] File {file_name} còn mới, dùng cache local.")
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_faiss_index_with_cache(service, FOLDER_ID, file_name="thathinh.index"):
    if is_file_expired(file_name):
        print(f"[Cache] File {file_name} đã cũ hoặc không tồn tại, tải lại từ Drive...")
        file_id = du.find_file_id(service, FOLDER_ID, file_name)
        if not file_id:
            raise FileNotFoundError(f"Không tìm thấy {file_name} trong folder {FOLDER_ID}")
        du.download_file(service, file_id, file_name)
    else:
        print(f"[Cache] File {file_name} còn mới, dùng cache local.")
    return faiss.read_index(file_name)

def init_chatbot(service, FOLDER_ID):
    mapping = load_mapping_with_cache(service, FOLDER_ID)
    index = load_faiss_index_with_cache(service, FOLDER_ID)
    embedder = SentenceTransformer("keepitreal/vietnamese-sbert")
    return mapping, index, embedder

def query_rag(data, top_k=20, threshold=200.0):
    try:
        service = du.authenticate()
        user_input = data["text"]
        mapping = data["mapping"]
        index = data["index"]
        embedder = data['embedder']
        query_embedding = embedder.encode([user_input], convert_to_numpy=True)
        D, I = index.search(query_embedding, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if dist < threshold:
                results.append(mapping[idx])
        res =  results if results else ["Không tìm thấy kết quả phù hợp."]
        return jsonify({
            "ketqua": res
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Server Error"
        }), 500

