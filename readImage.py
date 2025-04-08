import cv2
import os
import json
import time
from dotenv import load_dotenv
from api_call import GeminiModel
from filter import Filter

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BLOCKED_KEYWORDS = os.getenv("BLOCKED_KEYWORDS").split(",")
REMOVED_KEYWORDS = os.getenv("REMOVED_KEYWORDS").split(",")
FOLDER_PATH = os.getenv("FOLDER_PATH")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

index = 1
start_index = 1
results = []
processed_images = []
output_json_path = "ocr_results.json"

if os.path.exists(output_json_path):
    with open(output_json_path, "r", encoding="utf-8") as f:
        try:
            results = json.load(f)
            start_index = results[-1]["stt"] + 1
        except Exception as e:
            print("Lỗi đọc file JSON:", e)
            results = []
print(len(results))
gemini_model = GeminiModel(api_key=API_KEY)

try:
    for file_name in os.listdir(FOLDER_PATH):
        if index < start_index:
            index += 1
            continue
        if file_name.endswith((".jpg", ".png", ".jpeg")):
            img_path = os.path.join(FOLDER_PATH, file_name)
            img = cv2.imread(img_path)
            print(f'{index}:  {img.shape}')
            if img is None or img.shape[0] == 0:
                print(f"Bỏ qua ảnh lỗi: {file_name}")
                continue
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
            output_img_path = os.path.join(OUTPUT_FOLDER, f'output_gray{index}.jpg')
            cv2.imwrite(output_img_path, thresholded)
            
            text = gemini_model.extract_text_from_image(output_img_path)
            if text is None:
                print("Hết API hoặc lỗi xảy ra. Lưu kết quả và thoát...")
                break
            
            # Clean the extracted text
            text = Filter.clean_text(text)
            if len(text) == 0:
                continue
            
            print(text)
            results.append({"stt": index, "text": text})
            processed_images.append(output_img_path)
            index += 1
            time.sleep(1) 

except Exception as e:
    print("Lỗi trong quá trình xử lý:", e)

finally:
    with open(output_json_path, "w", encoding="utf-8") as json_file: 
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    results = Filter.filter(BLOCKED_KEYWORDS, REMOVED_KEYWORDS, results)

    with open('final_result.json', "w", encoding="utf-8") as json_file: 
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print(f"Kết quả đã được lưu vào 'final_result.json'")
