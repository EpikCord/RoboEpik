from json import load

class Config:
    def __init__(self):
        with open("./config.json") as f:
            config = load(f)

        self.token = config["token"]
        self.gist_pat = config["gist_pat"]