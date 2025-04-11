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
        text = re.sub(r'\n+\.', '.', text)
        text = re.sub(r'\n{2,}', '\n', text)   
        text = re.sub(r'^\.+', '', text)
        text = re.sub(r'(^|\.\s*|\n)thả thính[\s:,-]*\n?', r'\1', text, flags=re.IGNORECASE)
        text = text.strip(" \n")
        return text

    @staticmethod
    def filter(BLOCKED_KEYWORDS, REMOVED_KEYWORDS, jsonArray):
        results = []
        try:
            for item in jsonArray:
                text = item.get('text')
                if len(text.split(':')) == 3:
                    keyword = []
                    text = text.lower()

                    if Filter.contain(text, 'văn bản'):
                        if Filter.contain(text,':'):
                            pre = text.split(':')[2]
                            keyword = pre.split('*')
                            keyword = [k.strip() for k in keyword if k.strip()]
                            keyword = [k.strip() for k in keyword if k.strip().lower() != "thả thính"]
                            text = text.split(':')[1]
                        else:
                            continue
                    
                    for kw in REMOVED_KEYWORDS:
                        text = text.replace(kw, '')

                    text = Filter.clean_text(text)
                    
                    if len(text) < 25 or Filter.contains_blocked_keywords(text, BLOCKED_KEYWORDS):
                        continue
                  
                    if keyword:
                        results.append({
                            "keyword": keyword,
                            "text": text
                        })
                    else:
                        continue
                else:
                    continue
        except Exception as e:
            print(e)
            results = []
        return results

    @staticmethod
    def simple_filter(jsonArray):
        results = []
        try:
            for item in jsonArray:
                text = item.get("text")
                if len(text.split(':')) == 2:
                    keyword = []
                    text = text.lower()
                    text = text.replace("ghi chú","")
                    text.strip()
                    supertext = text.split('\n')
                    for pair in supertext:
                        if len(pair.split("=")) == 2:
                            pre = pair.split("=")[0]
                            keyword = pre.split()
                        else:
                            continue

                        if keyword:
                            results.append({
                                "keyword": keyword,
                                "text": pair
                            })
                    else:
                        continue

                else:
                    continue
        except Exception as e:
            print(e)
            results = []
        return results