import google.generativeai as genai
import PIL.Image
import time, os
from dotenv import load_dotenv
load_dotenv()

class GeminiModel:
    def __init__(self, model_name="gemini-2.0-flash", api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def extract_text_from_image(self, 
    image_path, 
    prompt="""Nhận diện văn bản trong bức ảnh theo ngôn ngữ tiếng Việt (chỉ cần văn bản trong ảnh không cần dài dòng gì khác). 
        Sau đó hãy rút ra 2 đến 3 từ khoá liên quan từ đoạn văn bản nhận được. 
        Trả lời theo format:
        Văn bản trong ảnh:<văn bản>Từ khoá:<từ khoá 1>*<từ khoá 2>*<từ khoá 3>""",
    retries=3):
        for retry in range(retries):
            try:
                img = PIL.Image.open(image_path)
                response = self.model.generate_content([prompt, img])
                return response.text
            except Exception as e:
                print(f"Lỗi API hoặc kết nối ({retry + 1}/{retries}): {e}")
                if retry < retries - 1:
                    print("Đang thử lại sau 30 giây...")
                    time.sleep(30)
                else:
                    print("Hết số lần thử.")
        return None
