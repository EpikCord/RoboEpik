from .config import Config
from EpikCord import Client, Intents, MessageTextInput, MessageActionRow, Modal

class RoboEpik(Client):
    def __init__(self, config: Config):
        super().__init__(
            config.token,
            Intents().guilds.guild_messages.message_content.guild_members
        )

client = RoboEpik(Config())

@client.command(
    description = "A testing modal."
)
async def test_modal(interaction):
    await interaction.send_modal(Modal(title = "Testing!", custom_id="test_modal", components = MessageActionRow([MessageTextInput(custom_id="test_input", style = 1, label = "Foo.",placeholder="Enter something...")])))

client.login()