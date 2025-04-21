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

class ConfigData:
    def __init__(self, START_INDEX_SUPERVISE, START_INDEX_UNSUPERVISE):
        self.START_INDEX_SUPERVISE = START_INDEX_SUPERVISE
        self.START_INDEX_UNSUPERVISE = START_INDEX_UNSUPERVISE
    
    def to_dict(self):
        return {
            "START_INDEX_SUPERVISE": self.START_INDEX_SUPERVISE,
            "START_INDEX_UNSUPERVISE": self.START_INDEX_UNSUPERVISE
        }
    
    @staticmethod
    def from_dict(data):
        return ConfigData(
            START_INDEX_SUPERVISE = data.get("START_INDEX_SUPERVISE"),
            START_INDEX_UNSUPERVISE = data.get("START_INDEX_UNSUPERVISE")
        )