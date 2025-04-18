class SentenceData:
    def __init__(self,keyword, text):
        self.keyword = keyword
        self.text = text
    
    def to_dict(self):
        return {
            "keyword": self.keyword,
            "text": self.text 
        }

    @staticmethod
    def from_dict(data):
        return SentenceData(
            keyword = data.get("keyword", []),
            text = data.get("text")
        )