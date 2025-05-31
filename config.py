import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "API_KEY_GEMINI" : os.getenv("API_KEY_GEMINI"),
        "BLOCKED_KEYWORDS" : os.getenv("BLOCKED_KEYWORDS").split(","),
        "REMOVED_KEYWORDS" : os.getenv("REMOVED_KEYWORDS").split(","),
        "FOLDER_PATH_UNSUPERVISE" : os.getenv("FOLDER_PATH_UNSUPERVISE"),
        "FOLDER_PATH_SUPERVISE" : os.getenv("FOLDER_PATH_SUPERVISE"),
        "FOLDER_CLOUD_UNSUPERVISE" : os.getenv("FOLDER_CLOUD_UNSUPERVISE"),
        "FOLDER_CLOUD_SUPERVISE" : os.getenv("FOLDER_CLOUD_SUPERVISE"),
        "OUTPUT_JSON_PATH" : os.getenv("OUTPUT_JSON_PATH"),
        "OUTPUT_TEMP_PATH" : os.getenv("OUTPUT_TEMP_PATH"),
        "MONGODB_SERVER" : os.getenv("MONGODB_SERVER"),
        "CLOUD_NAME": os.getenv("CLOUD_NAME"),
        "API_SECRET": os.getenv("API_SECRET"),
        "API_KEY": os.getenv("API_KEY"),
        "API_ENVIRONMENT_VARIABLE": os.getenv("API_ENVIRONMENT_VARIABLE"),
        "GOOGLE_CREDENTIALS_JSON": os.getenv("GOOGLE_CREDENTIALS_JSON"),
        "FOLDER_ID": os.getenv("FOLDER_ID"),
        "SECRET_ADMIN": os.getenv("SECRET_ADMIN")
    }
    

if __name__ == '__main__':
    load_config