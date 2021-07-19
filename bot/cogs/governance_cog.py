from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
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

    @cog_ext.cog_subcommand(
        base="proposal",
        subcommand_group="get",
        name="details",
        description="Get details of given proposal",
        options=[
            create_option(
                name="id",
                description="Id of the proposal",
                option_type=SlashCommandOptionType.INTEGER,
                required=True,
            ),
        ],
    )
    async def proposal(
        self,
        ctx: SlashContext,
        id: int,
    ):
        await ping_api(ctx)
        await governance_commands.proposal(
            self,
            ctx,
            id,
        )


def setup(bot):
    bot.add_cog(Governance(bot))
