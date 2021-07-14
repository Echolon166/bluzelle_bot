import sys
import traceback

from discord.ext import commands

import errors
from utils.converters import CryptoCoin
from utils import pretty_print
from constants import *
from apis import bluzelle_api, coingecko_api


class ChannelCommands(commands.Cog):
    """
    Cog for processing commands from a specific channel.
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
    async def crypto_price(
        self,
        ctx,
        coin: CryptoCoin = {
            "symbol": "BLZ",
            "data": coingecko_api.get_price_data("BLZ"),
        },
    ):
        if coin["data"] is None:
            raise errors.RequestError("There was an error while fetching the coin data")

        data = coin["data"]

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
            title=f"{coin['symbol']} Price Statistics",
            footer=self._requested_by_footer(ctx),
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="validators",
        help="Get the list of all active validators",
    )
    async def validators(self, ctx):
        validators = bluzelle_api.get_validators()
        if validators is None:
            raise errors.RequestError(
                "There was an error while fetching the validators"
            )

        validator_fields = []
        for validator in validators:
            validator_fields.append(
                {
                    "name": "Moniker",
                    "value": validator["moniker"],
                },
            )
            validator_fields.append(
                {
                    "name": "Address",
                    "value": validator["address"],
                },
            )
            validator_fields.append(
                {
                    "name": "Voting Power",
                    "value": f"{validator['voting_power']} ({validator['voting_power_percentage']})",
                },
            )

        await pretty_print(
            ctx,
            validator_fields,
            title="Validators",
            footer=self._requested_by_footer(ctx),
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="validator",
        help="Get the info of given validator",
    )
    async def validator(self, ctx, address: str):
        validator = bluzelle_api.get_validator(address)
        if validator is None:
            raise errors.RequestError("There was an error while fetching the validator")

        await pretty_print(
            ctx,
            [
                {
                    "name": "Identity",
                    "value": validator["identity"],
                    "inline": False,
                },
                {
                    "name": "Website",
                    "value": validator["website"],
                    "inline": False,
                },
                {
                    "name": "Security Contact",
                    "value": validator["security_contact"],
                    "inline": False,
                },
                {
                    "name": "Details",
                    "value": validator["details"],
                    "inline": False,
                },
                {
                    "name": "Voting Power",
                    "value": f"{validator['voting_power']} ({validator['voting_power_percentage']})",
                },
                {
                    "name": "Tokens",
                    "value": validator["tokens"],
                },
                {
                    "name": "Delegator Shares",
                    "value": validator["delegator_shares"],
                },
                {
                    "name": "Commission Rate",
                    "value": validator["commission_rate"],
                },
                {
                    "name": "Max Rate",
                    "value": validator["max_rate"],
                },
                {
                    "name": "Max Change Rate,",
                    "value": validator["max_change_rate"],
                },
            ],
            title=f"Info of '{validator['moniker']}'",
            footer=self._requested_by_footer(ctx),
            timestamp=True,
            color=WHITE_COLOR,
        )

    def _requested_by_footer(self, ctx):
        # Return empty dict if in private message
        if ctx.guild is None:
            return {}

        # Return requested by author message and author avatar url if in guild
        return {
            "text": f"Requested by {ctx.author.name}",
            "icon_url": ctx.author.avatar_url,
        }
