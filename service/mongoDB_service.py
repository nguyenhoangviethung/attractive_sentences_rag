import os
from flask import jsonify
from bson import ObjectId
import cloudinary
from database.model import SentenceData, ConfigData
from database import connect_db
from config import load_config
from pymongo.errors import BulkWriteError
from service import cloudinary_service as cs
from utilities.middleware import MiddleWare as MW

CONFIG = load_config()

db = connect_db(CONFIG)

def get_config():
    doc = db.configData.find_one()
    if doc:
        config = ConfigData.from_dict(doc)
        return config.START_INDEX_UNSUPERVISE, config.START_INDEX_SUPERVISE
    else:
        return 1, 1

@MW.check_permission
def add_sentence(data, is_authorized = None):
    try:
        data['text'] = data['text'].strip()
        sentence = SentenceData.from_dict(data)
        
        if is_authorized:
            db.sentences.insert_one(sentence.to_dict())
        else:
            db.temp.insert_one(sentence.to_dict())
        return jsonify({
            "message": "Sentence added"
        }), 202

    except Exception as e:
        print(e)
        return jsonify({
            "message": "Failure"
        }), 406

def fetch_all_sentences_raw():
    sentences_cursor = db.sentences.find({}, {"_id": 0})
    sentences = [SentenceData.from_dict(s).__dict__ for s in sentences_cursor]
    return sentences

@MW.check_permission
def get_sentences(is_authorized):
    try:
        if is_authorized:
            sentences = fetch_all_sentences_raw()
            return jsonify(sentences), 200
        else:
            return jsonify({"message": "Have not permission"}), 401
    except:
        return jsonify({"message": "Server Error"}), 500

@MW.check_permission
def get_temp_sentences(is_authorized):
    try:
        if is_authorized:
            sentences_cursor = db.temp.find({})  
            sentences = []
            for s in sentences_cursor:
                sentence_dict = SentenceData.from_dict(s).__dict__
                sentence_dict["_id"] = str(s["_id"])  
                sentences.append(sentence_dict)
            return jsonify(sentences), 200
        else:
            return jsonify({"message": "Have not permission"}), 401
    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500

@MW.check_permission
def pre_data(is_authorized):
    if not is_authorized:
        return jsonify({
            "message": "Have not permission"
        }), 401

    try:
        os.makedirs(CONFIG["FOLDER_PATH_UNSUPERVISE"], exist_ok=True)
        os.makedirs(CONFIG["FOLDER_PATH_SUPERVISE"], exist_ok=True)
        os.makedirs("data", exist_ok=True)

        sorted_images_unsupervise = cs.get_all_images(CONFIG["FOLDER_CLOUD_UNSUPERVISE"])
        sorted_images_supervise = cs.get_all_images(CONFIG["FOLDER_CLOUD_SUPERVISE"])

        from imageCollector.readImage import process_unsupervised_images, process_supervised_images
        i1, i2 = get_config()

        print(len(sorted_images_unsupervise))
        print(len(sorted_images_supervise))

        for i, item in enumerate(sorted_images_supervise[i2:]):
            cs.download_image(item["secure_url"], f'{CONFIG["FOLDER_PATH_SUPERVISE"]}/img{i+i2+1}.jpg')
        for i, item in enumerate(sorted_images_unsupervise[i1:]):
            cs.download_image(item["secure_url"], f'{CONFIG["FOLDER_PATH_UNSUPERVISE"]}/img{i+i1+1}.jpg')

        unsupervised, index_1 = process_unsupervised_images(
            config=CONFIG,
            model_name='gemini-2.0-flash',
            START_INDEX_UNSUPERVISE=i1
        )
        supervised, index_2 = process_supervised_images(
            config=CONFIG,
            model_name='gemini-2.0-flash',
            START_INDEX_SUPERVISE=i2
        )

        results = unsupervised + supervised

        config = ConfigData(
            START_INDEX_SUPERVISE=index_2,
            START_INDEX_UNSUPERVISE=index_1
        )
        db.configData.replace_one({}, config.to_dict(), upsert=True)

        documents = [SentenceData(item["keyword"], item["text"]).to_dict() for item in results]

        if not documents:
            return jsonify({"message": "No sentences to add"}), 200

        db.sentences.insert_many(documents, ordered=False)

        return jsonify({"message": "Sentences added"}), 200

    except BulkWriteError:
        return jsonify({"message": "Sentences added"}), 200

    except Exception as e:
        if "documents must be a non-empty list" in str(e):
            return jsonify({"message": "Sentences added"}), 200
        print(e)
        return jsonify({"message": "Sentence isn't added"}), 500

@MW.check_permission
def approve_text(data, is_authorized=None):
    if not is_authorized:
        return jsonify({"message": "Have not permission"}), 401
    
    try:
        id_str = data.get("_id")

        if not id_str:
            return jsonify({"message": "Missing _id"}), 400

        try:
            _id = ObjectId(id_str)
        except:
            return jsonify({"message": "Invalid _id format"}), 400

        temp_sentence = db.temp.find_one({"_id": _id})
        if not temp_sentence:
            return jsonify({"message": "Sentence not found"}), 404

        response, status = add_sentence(temp_sentence)
        if status != 202:
            return jsonify({"message": "Failed to add sentence during approval"}), 500

        delete_result = db.temp.delete_one({"_id": _id})
        if delete_result.deleted_count == 0:
            return jsonify({"message": "Sentence approved but failed to delete from temp"}), 206
        
        return jsonify({"message": "Sentence approved and moved"}), 200

    except Exception as e:
        print("Approve text failed:", e)
        return jsonify({"message": "Failed to approve sentence"}), 500

@MW.check_permission
def delete_temp_sentence(data, is_authorized=None):
    if not is_authorized:
        return jsonify({"message": "Have not permission"}), 401

    try:
        id_str = data.get("_id")

        if not id_str:
            return jsonify({"message": "Missing _id"}), 400

        try:
            _id = ObjectId(id_str)
        except:
            return jsonify({"message": "Invalid _id format"}), 400

        delete_result = db.temp.delete_one({"_id": _id})
        if delete_result.deleted_count == 0:
            return jsonify({"message": "Sentence not found or already deleted"}), 404

        return jsonify({"message": "Sentence deleted from temp"}), 200

    except Exception as e:
        print("Delete temp sentence failed:", e)
        return jsonify({"message": "Failed to delete sentence"}), 500
