from EpikCord import CommandUtils, Section, Button, ButtonStyle, Embed, ActionRow
from ..checks import is_untraceable

command_utils = CommandUtils()


class AnonymousHelp(Section):
    def __init__(self, client):
        self.client = client

    @command_utils.command(description="A command to delete a help channel thread.")
    async def delete_help_thread(self, interaction):
        await interaction.channel.delete_thread(interaction.thread_id)
        await interaction.reply(content="Thread deleted.")

    @command_utils.command(
        description="A command to setup the Anonymous help channel.",
        checks=[is_untraceable],
    )
    async def setup_anonymous(self, interaction):
        components = [
            ActionRow(
                [
                    Button(
                        label="Click here for Anonymous help!",
                        custom_id="anonymous_help",
                        style=ButtonStyle.GREEN,
                    )
                ]
            )
        ]
        embeds = [
            Embed(
                title="Anonymous help",
                description="Click the button below to setup the Anonymous help channel.",
                color=0x00FF00,
                footer={
                    "text": "No logs are kept of what is sent to who, and you can use the other help channels if you're comfortable with revealing your identity."
                },
            )
        ]
        await interaction.reply(embeds=embeds, components=components)
