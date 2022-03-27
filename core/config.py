from json import load

class Config:
    with open("config.json") as config_file:
        config = load(config_file)
    token = config["token"]
    pastebin_token = config["pastebin_key"]