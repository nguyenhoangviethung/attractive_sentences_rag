import json, os
from flask import jsonify
import faiss
from sentence_transformers import SentenceTransformer
from service import mongoDB_service as ms
from chatbot import drive_utils as du           
from utilities.middleware import MiddleWare as MW
from config import load_config
CONFIG = load_config()

FOLDER_ID = CONFIG["FOLDER_ID"]

@MW.check_permission
def build_index(mapping_file="mapping.json", index_file="thathinh.index", is_authorized=None, FOLDER_ID=FOLDER_ID):
    if not is_authorized:
        return jsonify({"message": "Have not permission"}), 401

    try:
        data = ms.fetch_all_sentences_raw()
        model = SentenceTransformer("keepitreal/vietnamese-sbert")

        corpus, mapping = [], []
        for item in data:
            keywords = ", ".join(item.get("keyword", []))
            full_text = f"{keywords} - {item.get('text', '')}"
            corpus.append(full_text)
            mapping.append(item.get("text", ""))

        embeddings = model.encode(corpus, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        # Lưu local
        faiss.write_index(index, index_file)
        with open(mapping_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False)

        print(f"✅ Đã tạo và lưu local: {mapping_file} và {index_file}")

        # Upload lên Google Drive
        service = du.authenticate()
        du.upload_file_to_folder(service, FOLDER_ID, mapping_file)
        du.upload_file_to_folder(service, FOLDER_ID, index_file)
        print("☁️ Đã upload lên Google Drive.")

        os.remove('mapping.json')
        os.remove('thathinh.index')

        return jsonify({"message": "Build index successfully"}), 202

    except Exception as e:
        print("❌ Lỗi:", e)
        return jsonify({"message": "Build index failure"}), 500
