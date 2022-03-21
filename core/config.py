from json import load

class Config:
    def __init__(self):
        with open("config.json") as f:
            self.config = load(f)
    
    @property
    def token(self):
        return self.config.get("token")