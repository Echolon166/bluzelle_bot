from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from cogs.commands import ping_api


from constants import *
import cogs.commands.governance_commands as governance_commands


class Governance(commands.Cog):
    """
    Governance related commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="proposal",
        subcommand_group="get",
        name="all",
        description="Get the list of all proposals",
    )
    async def proposals(self, ctx: SlashContext):
        await ping_api(ctx)
        await governance_commands.proposals(self, ctx)


def setup(bot):
    bot.add_cog(Governance(bot))
