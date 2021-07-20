from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from cogs.commands import ping_api

import cogs.commands.block_commands as block_commands


class Block(commands.Cog):
    """
    Block related commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="block",
        description="Get a block at a certain heigh (Default = Latest)",
        options=[
            create_option(
                name="height",
                description="The block height to get",
                option_type=SlashCommandOptionType.STRING,
                required=False,
            ),
        ],
    )
    async def block(self, ctx: SlashContext, height: str = "latest"):
        await ping_api(ctx)
        await block_commands.block(self, ctx, height)

    @cog_ext.cog_slash(
        name="consensus_state",
        description="Get the consensus state",
    )
    async def consensus_state(self, ctx: SlashContext):
        await ping_api(ctx)
        await block_commands.consensus_state(self, ctx)


def setup(bot):
    bot.add_cog(Block(bot))
