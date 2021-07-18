import sys
import traceback

from discord.ext import commands

import errors
from constants import *
from utils import pretty_print, requested_by_footer
from utils.converters import AccountAddress, CryptoCoin
from apis import coingecko_api
from apis.bluzelle_api import economy as economy_api


class Economy(commands.Cog):
    """
    Economy related commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @errors.standart_error_handler
    async def cog_command_error(self, ctx, error):
        """
        A special method that is called whenever an error is dispatched inside this cog.
        This is similar to on_command_error() except only applying to the commands inside this cog.

        Args:
            ctx (Context): The invocation context where the error happened.
            error (CommandError): The error that happened.
        """

        print(
            "Ignoring exception in command {}:".format(ctx.command),
            file=sys.stderr,
        )

        traceback.print_exception(
            type(error),
            error,
            error.__traceback__,
            file=sys.stderr,
        )

    @commands.command(
        name="price",
        help="Get the price of a crypto coin",
    )
    async def price(
        self,
        ctx,
        coin: CryptoCoin = BLZ_SYMBOL,
    ):
        # Retrieve the price data of the coin
        data = coingecko_api.get_price_data(coin)
        if data is None:
            raise errors.RequestError("There was an error while fetching the coin data")

        price_change_perc_24h = data["price_change_percentage_24h"]
        price_change_perc_7d = data["price_change_percentage_7d"]
        price_change_perc_30d = data["price_change_percentage_30d"]

        # Add + in front of the positive percentages to show green color (- comes from api itself for negatives)
        if price_change_perc_24h >= 0:
            price_change_perc_24h = "+" + str(price_change_perc_24h)
        if price_change_perc_7d >= 0:
            price_change_perc_7d = "+" + str(price_change_perc_7d)
        if price_change_perc_30d >= 0:
            price_change_perc_30d = "+" + str(price_change_perc_30d)

        await pretty_print(
            ctx,
            [
                {
                    "name": "Current Price",
                    "value": f"```diff\n${data['current_price']}```",
                    "inline": False,
                },
                {
                    "name": "24h Price Change",
                    "value": f"```diff\n{price_change_perc_24h}%\n```",
                },
                {
                    "name": "7d Price Change",
                    "value": f"```diff\n{price_change_perc_7d}%```",
                },
                {
                    "name": "30d Price Change",
                    "value": f"```diff\n{price_change_perc_30d}%```",
                },
                {
                    "name": "24h Low",
                    "value": f"```diff\n{data['low_24h']}```",
                },
                {
                    "name": "24h High",
                    "value": f"```diff\n{data['high_24h']}```",
                },
                {
                    "name": "Market Cap Rank",
                    "value": f"```diff\n{data['market_cap_rank']}```",
                },
            ],
            title=f"{coin} Price Statistics",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="balance",
        help="Get balance of an account",
    )
    async def balance(
        self,
        ctx,
        address: AccountAddress,
    ):
        balances = economy_api.get_balances(address)
        if balances is None:
            raise errors.RequestError("There was an error while fetching the balances")

        balance_fields = []
        for balance in balances:
            balance_fields.extend(
                [
                    {
                        "name": "Denom",
                        "value": balance["denom"],
                    },
                    {
                        "name": "Amount",
                        "value": balance["amount"],
                    },
                    {
                        "name": "\u200b",
                        "value": "\u200b",
                    },
                ]
            )

        await pretty_print(
            ctx,
            balance_fields,
            title=f"Balances of {address}",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="inflation",
        help="Get current minting inflation value",
    )
    async def inflation(self, ctx):
        inflation = economy_api.get_inflation()
        if inflation is None:
            raise errors.RequestError("There was an error while fetching the inflation")

        await pretty_print(
            ctx,
            [
                {
                    "name": "Current minting inflation value",
                    "value": inflation,
                },
            ],
            title="Inflation",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="community_pool",
        help="Get community pool coins",
    )
    async def community_pool(self, ctx):
        pools = economy_api.get_community_pools()
        if pools is None:
            raise errors.RequestError(
                "There was an error while fetching the community pool"
            )

        pool_fields = []
        for pool in pools:
            pool_fields.extend(
                [
                    {
                        "name": "Denom",
                        "value": pool["denom"],
                    },
                    {
                        "name": "Amount",
                        "value": pool["amount"],
                    },
                    {
                        "name": "\u200b",
                        "value": "\u200b",
                    },
                ]
            )

        await pretty_print(
            ctx,
            pool_fields,
            title="Community Pool",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )
