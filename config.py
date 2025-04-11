import os
from dotenv import load_dotenv
from api_call import GeminiModel

def load_config():
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    BLOCKED_KEYWORDS = os.getenv("BLOCKED_KEYWORDS").split(",")
    REMOVED_KEYWORDS = os.getenv("REMOVED_KEYWORDS").split(",")
    FOLDER_PATH_UNSUPERVISE = os.getenv("FOLDER_PATH_UNSUPERVISE")
    FOLDER_PATH_SUPERVISE = os.getenv("FOLDER_PATH_SUPERVISE")
    OUTPUT_JSON_PATH = os.getenv("OUTPUT_JSON_PATH")
    OUTPUT_TEMP_PATH = os.getenv("OUTPUT_TEMP_PATH")

    return {
        "API_KEY": API_KEY,
        "BLOCKED_KEYWORDS": BLOCKED_KEYWORDS,
        "REMOVED_KEYWORDS": REMOVED_KEYWORDS,
        "FOLDER_PATH_UNSUPERVISE": FOLDER_PATH_UNSUPERVISE,
        "FOLDER_PATH_SUPERVISE": FOLDER_PATH_SUPERVISE,
        "OUTPUT_JSON_PATH": OUTPUT_JSON_PATH,
        "OUTPUT_TEMP_PATH": OUTPUT_TEMP_PATH
    }

if __name__ == '__main__':
    load_config