from dotenv import load_dotenv
import os, json
from filter import Filter
from api_call import GeminiModel
load_dotenv()

start_index = input()
index = 1
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
