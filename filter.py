from dotenv import load_dotenv
import os, json, re

load_dotenv()

class Filter:
    @staticmethod
    def contains_blocked_keywords(text, BLOCKED_KEYWORDS):
        lowered = text.lower()
        return any(keyword in lowered for keyword in BLOCKED_KEYWORDS)

    @staticmethod
    def contain(text, keyword):
        return keyword in text.lower()

    @staticmethod
    def clean_text(text):
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\S\r\n]+', ' ', text).strip()
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\n?"{2,}\n?', '', text)
        return text

    @staticmethod
    def filter(BLOCKED_KEYWORDS, REMOVED_KEYWORDS, jsonArray):
        results = []
        index = 1
        try:
            for item in jsonArray:
                text = item.get('text')
                text = text.lower()
                if Filter.contain(text, 'văn bản'):
                    if Filter.contain(text,':'):
                        text = text.split(':')[1]
                    else:
                        continue
                if len(text) < 25 or Filter.contains_blocked_keywords(text, BLOCKED_KEYWORDS):
                    print(text)
                    print('----------------------------------------------------')
                    continue
                if Filter.contain(text, 'văn bản'):
                    continue
                for keyword in REMOVED_KEYWORDS:
                    text = text.replace(keyword, '')
                text = re.sub(r'\n\s*\n+', '\n', text)
                
                results.append({
                    "stt": index,
                    "text": text
                })
                index += 1
        except Exception as e:
            print(e)
            results = []
        return results

    # with open(results_path, "w", encoding="utf-8") as json_file:
    #     json.dump(results, json_file, ensure_ascii=False, indent=4)

    # print(f"Kết quả đã được lưu vào {results_path}")
