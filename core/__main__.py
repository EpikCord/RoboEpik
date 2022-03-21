from .config import Config
from EpikCord import Client, Intents

class RoboEpik(Client):
    def __init__(self, config: Config):
        super().__init__(
            config.token,
            Intents().guilds.guild_messages.message_content.guild_members
        )

client = RoboEpik(Config())
client.login()