from datetime import timedelta, datetime
from asyncio import create_task
from .config import Config
from EpikCord import ActionRow, Modal, TextInput, Embed, ModalSubmitInteraction, Message
from EpikCord.ext.tasks import task
from .bot import RoboEpik
client = RoboEpik(Config())

@client.event()
async def ready():
    print("Ready!")

@client.command_utils.check
async def is_untraceable(interaction):
    return interaction.author.id == "507969622876618754"

@is_untraceable.success
async def is_untraceable_success(interaction):
    client.logger.debug(f"Untraceable detected with id {interaction.user.id}.")

@is_untraceable.failure
async def is_untraceable_failure(interaction):
    return await interaction.reply(content = "Only The Untraceable can run that command.")

@client.component("anonymous_help")
async def anonymous_help_button_click(interaction, _):
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
                        required = True,
                        max_length=10
                )])
            ])
    )        

@client.component("anonymous_help_modal")
async def anonymous_help_modal_submit(interaction: ModalSubmitInteraction, code: str, issue_description: str, full_traceback: str, version: str):
    lines = ''.join('-' for _ in range(20))
    pastebin_link = await client.create_pastebin(f"#{lines} CODE {lines}\n\n\n{code}\n\n\n#{lines} FULL TRACEBACK {lines}\n{full_traceback}")
    embed = [
        Embed(
            title = "Anonymous help",
            description = f"Your issue has been submitted to the Anonymous help channel. Your code has been posted [here]({pastebin_link})",
            color = 0x00ff00,
            footer = {"text": "No logs are kept of what is sent to who, and you can use the other help channels if you're comfortable with revealing your identity."}
        )
    ]
    await interaction.reply(embeds = embed, ephemeral=True)
    thread = await (await client.channels.fetch(interaction.channel_id)).start_thread(issue_description[:100] if len(issue_description) <= 100 else f"{issue_description[:97]}...", type = 11)

    await thread.send(f"Code and full traceback: {pastebin_link}\nIssue description: {issue_description}\nEpikCord Version: {version}")

@client.event()
async def message_create(message: Message):
    if message.type == 18:
        await message.delete(reason="Message is a thread create message.")

@task(hours=24)
async def clean_up_gists():
    client.logger.debug("Cleaning up gists...")
    response = await client.http.get("https://api.github.com/gists?per_page=100", to_discord = False, headers = {
        "User-Agent": "RoboEpik",
        "Authorization": f"token {client.config.gist_pat}"
    })
    body = await response.json()
    for gist in body:
        if datetime.fromisoformat(gist["created_at"]) < (datetime.now() - timedelta(days=1)).isoformat():
            client.logger.info(f"Deleting gist {gist['id']}...")
            create_task(client.http.delete(f"https://api.github.com/gists/{gist['id']}", to_discord = False, headers = {
                "User-Agent": "RoboEpik",
                "Authorization": f"token {client.config.gist_pat}"
            }))

client.login()