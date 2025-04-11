from readImage import process_unsupervised_images, process_supervised_images
from config import load_config
import json

CONFIG = load_config()
unsupervised = process_unsupervised_images(config = CONFIG, model_name='gemini-2.0-flash-lite')
supervised = process_supervised_images(config = CONFIG,model_name='gemini-2.0-flash-lite')
results = unsupervised + supervised

with open('data/data.json', 'w', encoding = 'utf-8') as f:
    json.dump(results, f, ensure_ascii = False, indent = 4)
print("Xong!!")
