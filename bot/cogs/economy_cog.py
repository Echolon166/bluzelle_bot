from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from cogs.commands import ping_api

from constants import *
import utils.converters as converters
import cogs.commands.economy_commands as economy_commands


class Economy(commands.Cog):
    """
    Economy related commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="price",
        description="Get the price of a crypto coin (Default = BLZ)",
        options=[
            create_option(
                name="coin",
                description="Symbol of the coin (Such as BLZ)",
                option_type=SlashCommandOptionType.STRING,
                required=False,
            ),
        ],
    )
    async def price(
        self,
        ctx: SlashContext,
        coin: converters.CryptoCoin = BLZ_SYMBOL,
    ):
        await ping_api(ctx)

        coin = await converters.CryptoCoin.convert(self, ctx, coin)
        await economy_commands.price(self, ctx, coin)

    @cog_ext.cog_slash(
        name="balance",
        description="Get balance of an account",
        options=[
            create_option(
                name="address",
                description="Address of the account",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def balance(
        self,
        ctx: SlashContext,
        address: converters.AccountAddress,
    ):
        await ping_api(ctx)

        address = await converters.AccountAddress.convert(self, ctx, address)
        await economy_commands.balance(self, ctx, address)

    @cog_ext.cog_slash(
        name="inflation",
        description="Get current minting inflation value",
    )
    async def inflation(self, ctx: SlashContext):
        await ping_api(ctx)
        await economy_commands.inflation(self, ctx)

    @cog_ext.cog_slash(
        name="community_pool",
        description="Get community pool coins",
    )
    async def community_pool(self, ctx: SlashContext):
        await ping_api(ctx)
        await economy_commands.community_pool(self, ctx)


def setup(bot):
    bot.add_cog(Economy(bot))
