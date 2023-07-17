import json

STATUS_INIT = "INIT"
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"

class ClassifierResult:        
    def __init__(self, imgPath):
        self.imgPath = imgPath
        self.tags = []
        self.captions = []
        self.texts = []
        self.status = "INIT"

    def to_json_string(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return {"imgPath": self.imgPath, "tags": self.tags, "captions": self.captions, "texts": self.texts, "status": self.status}

    def add_tag(self, name, conf):
        self.tags.append({
            "name": name,
            "conf": conf,
        })
    
    def add_caption(self, name, conf):
        self.captions.append({
            "name": name,
            "conf": conf,
        })
    def add_text(self, text):
        self.texts.append(text)
    
