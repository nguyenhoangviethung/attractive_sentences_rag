
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def connect_db(CONFIG):
    uri = CONFIG["MONGODB_SERVER"]
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["FunnySentence"]
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return db