from EpikCord import Client, Intents
from json import load

class Config:
    def __init__(self):
        with open('config.json') as f:
            self.data = load(f)
        
    @property
    def token(self):
        return self.data['token']

class RoboEpik(Client):

    def __init__(self):
        self.config = Config()

        super().__init__(self.config.token, Intents().all.remove_intent("guild_presences"))

client = RoboEpik()

@client.event
async def ready():
    print("Ready!")


client.login()