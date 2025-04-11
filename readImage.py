import cv2, os, json, time
from dotenv import load_dotenv
from api_call import GeminiModel
from filter import Filter

def process_unsupervised_images(config, model_name = 'gemini-2.0-flash'):
    API_KEY = config["API_KEY"]
    BLOCKED_KEYWORDS = config["BLOCKED_KEYWORDS"]
    REMOVED_KEYWORDS = config["REMOVED_KEYWORDS"]
    FOLDER_PATH_UNSUPERVISE = config["FOLDER_PATH_UNSUPERVISE"]
    OUTPUT_JSON_PATH = config["OUTPUT_JSON_PATH"]

    gemini_model = GeminiModel(model_name, api_key = API_KEY)

    index = 1
    start_index = 1
    results = []

    if os.path.exists(OUTPUT_JSON_PATH):
        with open(OUTPUT_JSON_PATH, "r", encoding="utf-8") as f:
            try:
                results = json.load(f)
                start_index = results[-1]["stt"] + 1
            except Exception as e:
                print("Lỗi đọc file JSON:", e)
                results = []

    try:
        files = sorted(
            os.listdir(FOLDER_PATH_UNSUPERVISE),
            key=lambda x: os.path.getmtime(os.path.join(FOLDER_PATH_UNSUPERVISE, x))
        )
        for file_name in files:
            if index < start_index:
                index += 1
                continue

            if file_name.endswith((".jpg", ".png", ".jpeg")):
                img_path = os.path.join(FOLDER_PATH_UNSUPERVISE, file_name)
                img = cv2.imread(img_path)
                if img is None or img.shape[0] == 0:
                    print(f"Bỏ qua ảnh lỗi: {file_name}")
                    continue

                print(f'{index}:  {img.shape}')
                text = gemini_model.extract_text_from_image(img_path)
                if text is None:
                    print("Hết API hoặc lỗi xảy ra. Lưu kết quả và thoát...")
                    break

                text = Filter.clean_text(text)
                if len(text) == 0:
                    continue

                print(text)
                results.append({"stt": index, "text": text})
                index += 1
                time.sleep(2)

    except Exception as e:
        print("Lỗi trong quá trình xử lý:", e)

    finally:
        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)

        results = Filter.filter(BLOCKED_KEYWORDS, REMOVED_KEYWORDS, results)

        with open('data/final_result.json', "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)

        print(f"Kết quả đã được lưu vào 'data/final_result.json'")
        return results

def process_supervised_images(config, model_name='gemini-2.0-flash'):
    API_KEY = config["API_KEY"]
    FOLDER_PATH_SUPERVISE = config["FOLDER_PATH_SUPERVISE"]
    OUTPUT_JSON_PATH = config["OUTPUT_JSON_PATH"]
    OUTPUT_TEMP_PATH = config["OUTPUT_TEMP_PATH"]
    gemini_model = GeminiModel(model_name, api_key = API_KEY)

    index = 1
    start_index = 1
    results = []

    if os.path.exists(OUTPUT_TEMP_PATH):
        with open(OUTPUT_TEMP_PATH, "r", encoding="utf-8") as f:
            try:
                results = json.load(f)
                start_index = results[-1]["stt"] + 1
            except Exception as e:
                print("Lỗi đọc file JSON:", e)
                results = []
    try:
        files = sorted(
            os.listdir(FOLDER_PATH_SUPERVISE),
            key = lambda x : os.path.getmtime(os.path.join(FOLDER_PATH_SUPERVISE,x))
        )
        for file_name in files:
            if index < start_index:
                index += 1
                continue

            if file_name.endswith((".jpg", ".png", ".jpeg")):
                img_path = os.path.join(FOLDER_PATH_SUPERVISE, file_name)
                img = cv2.imread(img_path)
                if img is None or img.shape[0] == 0:
                    print(f"Bỏ qua ảnh lỗi: {file_name}")
                    continue

                print(f'{index}:  {img.shape}')
                text = gemini_model.extract_text_from_image(
                    img_path,
                    prompt = """Nhận diện văn bản trong bức ảnh theo ngôn ngữ tiếng Việt (chỉ cần văn bản trong ảnh không cần dài dòng gì khác)
                    Trả lời theo format:
                    Văn bản trong ảnh:<văn bản>"""
                )
                if text is None:
                    print("Hết API hoặc lỗi xảy ra. Lưu kết quả và thoát...")
                    break

                text = Filter.clean_text(text)
                if len(text) == 0:
                    continue

                print(text)
                results.append({"stt": index, "text": text})
                index += 1
                time.sleep(2)

    except Exception as e:
        print("Lỗi trong quá trình xử lý:", e)

    finally:
        with open(OUTPUT_TEMP_PATH, "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)

        results = Filter.simple_filter(results)

        with open('data/final1_result.json', "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)

        print(f"Kết quả đã được lưu vào 'data/output_temp.json'")
        return results
if __name__ == "__main__":
    process_unsupervised_images()
    process_supervised_images()
