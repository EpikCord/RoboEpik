from EpikCord import CommandUtils, Intents, Client
from .config import Config
from logging import getLogger, FileHandler, Formatter


class RoboEpik(Client):
    def __init__(self, config: Config):
        intents = Intents()

        intents.guilds = True
        intents.guild_messages = True
        intents.message_content = True
        intents.guild_members = True

        super().__init__(config.token, intents, overwrite_commands_on_ready=False)
        self.commands = {}
        self.command_utils: CommandUtils = CommandUtils()
        self.config = config
        self.logger = getLogger("EpikCord")
        self.logger.setLevel(-100)  # Catch all.
        handler = FileHandler(filename="RoboEpikLogs.log", encoding="utf-8", mode="w")
        self.handler.setFormatter(
            Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
        )
        self.logger.addHandler(handler)

    async def create_pastebin(self, code: str):

        response = await self.http.post(
            "https://api.github.com/gists",
            to_discord=False,
            json={
                "description": "Code posted from EpikCord's Anonymous Help system.",
                "public": False,
                "files": {"main.py": {"content": code}},
            },
            headers={
                "User-Agent": "RoboEpik",
                "Authorization": f"token {self.config.gist_pat}",
            },
        )

        # TODO: Add support for Ratelimit handling.
        body = await response.json()

        return body["html_url"]
