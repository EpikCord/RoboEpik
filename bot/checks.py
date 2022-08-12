from EpikCord import CommandUtils


@CommandUtils.check
async def is_untraceable(interaction):
    return interaction.author.id == "507969622876618754"


@is_untraceable.success
async def is_untraceable_success(interaction):
    interaction.client.logger.debug(
        f"Untraceable detected with id {interaction.user.id}."
    )


@is_untraceable.failure
async def is_untraceable_failure(interaction):
    return await interaction.reply(content="Only The Untraceable can run that command.")
