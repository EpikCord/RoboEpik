from .config import Config
from EpikCord import Client, Intents
from re import compile

PULL_HASH_REGEX = compile(r'(?:(?P<org>(?:[A-Za-z]|\d|-)+)/)?(?P<repo>(?:[A-Za-z]|\d|-)+)?(?:##)(?P<index>[0-9]+)')

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
    
    def make_link(index, org=None, repo=None):
        org = org or "Pycord-Development"
        repo = repo or "pycord"
        return f"https://github.com/{org}/{repo}/pull/{index}"

    async def message_create(self, message):
        links = list(set([self.make_link(index, org, repo) for org, repo, index in PULL_HASH_REGEX.findall(message.content)]))[:15]
        if len(links) > 2:
            links = [f"<{link}>" for link in links]
        if links:
            await message.reply("\n".join(links))