from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from cogs.commands import ping_api


from constants import *
import utils.converters as converters
import cogs.commands.validator_commands as validator_commands


class Validator(commands.Cog):
    """
    Validator related commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="validator",
        subcommand_group="get",
        name="all",
        description="Get the list of all validators",
    )
    async def validators(self, ctx: SlashContext):
        await ping_api(ctx)
        await validator_commands.validators(self, ctx)

    @cog_ext.cog_subcommand(
        base="validator",
        subcommand_group="get",
        name="details",
        description="Get details of given validator",
        options=[
            create_option(
                name="address",
                description="Address of the validator",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def validator(
        self,
        ctx: SlashContext,
        address: converters.ValidatorAddress,
    ):
        await ping_api(ctx)

        address = await converters.ValidatorAddress.convert(self, ctx, address)
        await validator_commands.validator(self, ctx, address)

    @cog_ext.cog_subcommand(
        base="validator",
        subcommand_group="get",
        name="delegations",
        description="Get delegations of given validator",
        options=[
            create_option(
                name="address",
                description="Address of the validator",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def delegations(
        self,
        ctx: SlashContext,
        address: converters.ValidatorAddress,
    ):
        await ping_api(ctx)

        address = await converters.ValidatorAddress.convert(self, ctx, address)
        await validator_commands.delegations(self, ctx, address)


def setup(bot):
    bot.add_cog(Validator(bot))
