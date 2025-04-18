from flask import Flask, request, jsonify
from database import connect_db
from database.model import SentenceData

def create_app(CONFIG):
    app = Flask(__name__)
    db = connect_db(CONFIG)
    pipeline = [
            {"$group": {"_id": "$text", "dups": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]

    duplicates = list(db.sentences.aggregate(pipeline))
    for doc in duplicates:
        ids_to_delete = doc["dups"][1:]
        db.sentences.delete_many({"_id": {"$in": ids_to_delete}})
    try:
        db.sentences.create_index("text", unique = True)
    except:
        pass
    @app.route('/')
    def index():
        return "Hello world"

    @app.post('/add-sentence')
    def add_sentence():
        data = request.json
        data['text'] = data['text'].strip()
        sentecce = SentenceData.from_dict(data)
        try:
            db.sentences.insert_one(sentecce.to_dict())
        except:
            pass
        finally:
            return jsonify({
                "message": "Sentence added"
            })
    
    @app.get('/sentences')
    def get_sentences():
        sentences_cursor = db.sentences.find({}, {"_id": 0})
        sentences = [SentenceData.from_dict(s).__dict__ for s in sentences_cursor]
        return jsonify(sentences)

    @app.route('/pre-data')
    def pre_data():
        from imageCollector.readImage import process_unsupervised_images, process_supervised_images
        unsupervised = process_unsupervised_images(config = CONFIG, model_name='gemini-2.0-flash')
        supervised = process_supervised_images(config = CONFIG,model_name='gemini-2.0')
        results = unsupervised + supervised

        try:
            documents = [SentenceData(item["keyword"], item["text"]).to_dict() for item in results]
            db.sentences.insert_many(documents, ordered = False)
        except:
            pass
        finally:
            return jsonify({
                "message": "Sentences added"
            })
    return app
