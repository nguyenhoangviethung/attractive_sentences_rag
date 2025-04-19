from flask import jsonify
from database.model import SentenceData
from database import connect_db
from config import load_config
from pymongo.errors import BulkWriteError
CONFIG = load_config()

db = connect_db(CONFIG)

def add_sentence(data):
    try:
        data['text'] = data['text'].strip()
        sentence = SentenceData.from_dict(data)
        db.sentences.insert_one(sentence.to_dict())
        
        return jsonify({
            "message": "Sentence added"
        }), 202

    except Exception as e:
        print(e)
        return jsonify({
            "message": "Failure"
        }), 406

def get_sentences():
    try:
        sentences_cursor = db.sentences.find({}, {"_id": 0})
        sentences = [SentenceData.from_dict(s).__dict__ for s in sentences_cursor]
        return jsonify(sentences), 200
    except:
        return jsonify({
            "message": "Server Error"
        }), 500

def pre_data():
    from imageCollector.readImage import process_unsupervised_images, process_supervised_images
    unsupervised = process_unsupervised_images(config = CONFIG, model_name='gemini-2.0-flash')
    supervised = process_supervised_images(config = CONFIG,model_name='gemini-2.0')
    results = unsupervised + supervised

    try:
        documents = [SentenceData(item["keyword"], item["text"]).to_dict() for item in results]
        db.sentences.insert_many(documents, ordered = False)

        return jsonify({
            "message": "Sentences added"
        }), 200
    except BulkWriteError as e:
        return jsonify({
            "message": "Sentences added"
        }), 200
    
    except Exception as e:
        return jsonify({
            "message": "Sentence isn't added"
        }), 500
        
        