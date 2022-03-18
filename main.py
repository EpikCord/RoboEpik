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
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.config = Config()
        self.intents = Intents().all

    async def connect(self):
        await super.connect(self.config.token, intents=Intents.all())
        self.token = None # Making sure in the worst case where there is a bug where you can access the RoboEpik class from Discord, the Token will not be leaked.
        self.config.token = None # Erasing it from Config too.

    async def on_ready(self):
        print(f"I am ready! My name is {self.user.name}")

client = RoboEpik()

client.login()