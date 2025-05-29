from flask import jsonify
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
    sorted_images_unsupervise = cs.get_all_images(CONFIG["FOLDER_CLOUD_UNSUPERVISE"])

    sorted_images_supervise = cs.get_all_images(CONFIG["FOLDER_CLOUD_SUPERVISE"])

    from imageCollector.readImage import process_unsupervised_images, process_supervised_images
    i1, i2 = get_config()
    print(len(sorted_images_unsupervise))
    print(len(sorted_images_supervise))
    for i, item in enumerate(sorted_images_supervise[i2::]):
        cs.download_image(item["secure_url"], CONFIG["FOLDER_PATH_SUPERVISE"] + f'/img{i+i2+1}' + '.jpg')
    for i, item in enumerate(sorted_images_unsupervise[i1::]):
        cs.download_image(item["secure_url"], CONFIG["FOLDER_PATH_UNSUPERVISE"] + f'/img{i+i1+1}' + '.jpg')
    unsupervised, index_1 = process_unsupervised_images(
        config = CONFIG, 
        model_name='gemini-2.0-flash',
        START_INDEX_UNSUPERVISE =  i1
    )
    supervised, index_2 = process_supervised_images(
        config = CONFIG,
        model_name='gemini-2.0-flash',
        START_INDEX_SUPERVISE = i2
    )
    results = unsupervised + supervised
    try:        
        config = ConfigData(START_INDEX_SUPERVISE=index_2, START_INDEX_UNSUPERVISE=index_1)
        db.configData.replace_one({}, config.to_dict(), upsert=True)
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
        print(e)
        return jsonify({
            "message": "Sentence isn't added"
        }), 500
        

