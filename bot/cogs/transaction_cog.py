from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from cogs.commands import ping_api

import cogs.commands.transaction_commands as transaction_commands


class Transaction(commands.Cog):
    """
    Transaction related commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="transaction",
        description="Get transaction details",
        options=[
            create_option(
                name="hash",
                description="# Hash of the transaction",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def transaction(self, ctx: SlashContext, hash: str):
        await ping_api(ctx)
        await transaction_commands.transaction(self, ctx, hash)


def setup(bot):
    bot.add_cog(Transaction(bot))
