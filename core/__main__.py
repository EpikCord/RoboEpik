import aiohttp
from config import Config
from EpikCord import Client, Intents, Button, ActionRow, Modal, ApplicationCommandInteraction, TextInput, Embed, Message
import logging

logger = logging.getLogger('EpikCord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='.\\epik.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
class RoboEpik(Client):
    def __init__(self, config: Config):
        super().__init__(
            config.token,
            Intents().guilds.guild_messages.message_content.guild_members
        )

    async def create_pastebin(self, code: str):
        ...

client = RoboEpik(Config())

@client.command(
    description = "A command to setup the Anonymous help channel.",
    guild_ids = ["937364424208039957"]
)
async def setup_anonymous(interaction: ApplicationCommandInteraction):
    if interaction.author.id != "507969622876618754":
        return await interaction.reply(content = "Only The Untraceable can run that command.")
    components = [
        ActionRow([
            Button(label="Click here for Anonymous help!", custom_id = "anonymous_help").GREEN
        ])
    ]
    embed = [
        Embed(
            title = "Anonymous help",
            description = "Click the button below to setup the Anonymous help channel.",
            color = 0x00ff00,
            footer = {"text": "No logs are kept of what is sent to who, and you can use the other help channels if you're comfortable with revealing your identity."}
        )
    ]
    await interaction.reply(embeds = embed, components = components)

@client.component("anonymous_help")
async def anonymous_help_button_click(interaction, button):
    await interaction.send_modal(
        Modal(
            custom_id = "anonymous_help_modal",
            title = "Anonymous help",
            components = [
                ActionRow([
                    TextInput(
                        custom_id = "code",
                        label = "Code",
                        placeholder = "Enter the code here.",
                        style = 2,
                        required = True
                    )
                ]), ActionRow([
                    TextInput(
                        custom_id = "issue_description",
                        label = "Issue description",
                        placeholder = "Enter the issue description here.",
                        style = 2,
                        required = True
                )]), ActionRow([
                    TextInput(
                        custom_id = "full_traceback",
                        label = "Full traceback",
                        placeholder = "Enter the full traceback here.",
                        style = 2,
                        required = True
                    )
                ]), ActionRow([
                    TextInput(
                        custom_id = "version",
                        label = "Version",
                        placeholder = "Enter EpikCord.py version here.",
                        style = 1,
                        required = True
                )])
            ])
    )        

@client.component("anonymous_help_modal")
async def anonymous_help_modal_submit(interaction, code, issue_description, full_traceback, version):
    if (len(code) + len(issue_description) + len(full_traceback) + len(version)) > 2000 and (len(issue_description) + len(full_traceback) + len(version)) < 2000:
        pastebin_link = await client.create_pastebin(code, full_traceback)
        embed = [
            Embed(
                title = "Anonymous help",
                description = f"Your issue has been submitted to the Anonymous help channel. Your code has been posted [here]({pastebin_link})",
                color = 0x00ff00,
                footer = {"text": "No logs are kept of what is sent to who, and you can use the other help channels if you're comfortable with revealing your identity."}
            )
        ]
        await interaction.reply(embeds = embed)
    await interaction.create_followup()

GH_API_SITE = "https://api.github.com"

@client.event
async def on_message_create(message:Message):
    if message.content.startswith("##") :#Represents a github issue
        gh_repo_id = message.content.strip("##")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{GH_API_SITE}/repos/EpikCord/EpikCord.py/issues/{gh_repo_id}") as resp:
                resp_stat = resp.status
                response: dict = await resp.json()
                title = response.get("title")
                user = response.get("user")
                user_name = user.get("login")
            
                body = response.get("body")
                url = response.get("url")
                
                if resp_stat == 200:

                    issue_or_pr_em = [Embed(title = f"Issue/PR {gh_repo_id}", description=f"Title = {title}\nBy: {user_name}\nBody: {body}", footer={"text":f"For more info, visit {url}"})]
                await message.channel.send(embeds=issue_or_pr_em)


client.login()