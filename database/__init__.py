
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import cloudinary

def connect_db(CONFIG):
    uri = CONFIG["MONGODB_SERVER"]
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["FunnySentence"]
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
    try:
        client.admin.command('ping')
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return db

def connect_cloudinary(CONFIG):
    cloudinary.config(
        cloud_name=CONFIG["CLOUD_NAME"],
        api_key=CONFIG["API_KEY"],
        api_secret=CONFIG["API_SECRET"],
        secure = True
    )
    print("✅ Connection to cloudinary successfully")
    

