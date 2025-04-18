import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "API_KEY" : os.getenv("API_KEY"),
        "BLOCKED_KEYWORDS" : os.getenv("BLOCKED_KEYWORDS").split(","),
        "REMOVED_KEYWORDS" : os.getenv("REMOVED_KEYWORDS").split(","),
        "FOLDER_PATH_UNSUPERVISE" : os.getenv("FOLDER_PATH_UNSUPERVISE"),
        "FOLDER_PATH_SUPERVISE" : os.getenv("FOLDER_PATH_SUPERVISE"),
        "OUTPUT_JSON_PATH" : os.getenv("OUTPUT_JSON_PATH"),
        "OUTPUT_TEMP_PATH" : os.getenv("OUTPUT_TEMP_PATH"),
        "MONGODB_SERVER" : os.getenv("MONGODB_SERVER")
    }
    

if __name__ == '__main__':
    load_config