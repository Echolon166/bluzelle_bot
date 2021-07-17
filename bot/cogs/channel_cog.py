import sys
import traceback

from discord.ext import commands

import errors
from utils.converters import CryptoCoin
from utils import pretty_print, requested_by_footer
from constants import *
from apis import coingecko_api
from apis.bluzelle_api import (
    block as block_api,
    economy as economy_api,
    validator as validator_api,
)


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
    async def price(
        self,
        ctx,
        coin: CryptoCoin = {
            "symbol": BLZ_SYMBOL,
            "data": coingecko_api.get_price_data(BLZ_SYMBOL),
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
    async def balance(self, ctx, address: str):
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

    @commands.command(
        name="validators",
        help="Get the list of all active validators",
    )
    async def validators(self, ctx):
        validators = validator_api.get_validators()
        if validators is None:
            raise errors.RequestError(
                "There was an error while fetching the validators"
            )

        active_validators = [
            d
            for d in validators
            if d["jailed"] == False and d["status"] == "BOND_STATUS_BONDED"
        ]

        validator_fields = []
        validator_fields.append(
            {
                "name": "Active Validators",
                "value": f"{len(active_validators)} out of {len(validators)} validators",
                "inline": False,
            },
        )
        for validator in active_validators:
            validator_fields.extend(
                [
                    {
                        "name": "Moniker",
                        "value": validator["moniker"],
                    },
                    {
                        "name": "Operator Address",
                        "value": validator["address"],
                    },
                    {
                        "name": "Voting Power",
                        "value": f"{validator['voting_power']} ({validator['voting_power_percentage']})",
                    },
                ]
            )

        await pretty_print(
            ctx,
            validator_fields,
            title="Validators",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="validator",
        help="Get the info of given validator",
    )
    async def validator(self, ctx, address: str):
        validator = validator_api.get_validator_by_address(address)
        if validator is None:
            raise errors.RequestError("There was an error while fetching the validator")

        await pretty_print(
            ctx,
            [
                {
                    "name": "Self-Delegate Address",
                    "value": validator["self_delegate_address"],
                },
                {
                    "name": "Self Delegation Ratio",
                    "value": validator["self_delegation_ratio"],
                },
                {
                    "name": "Proposer Priority",
                    "value": validator["proposer_priority"],
                },
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
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="delegations",
        help="Get delegations of given validator",
    )
    async def delegations(self, ctx, address: str):
        delegations = validator_api.get_validator_delegations(address)
        if delegations is None:
            raise errors.RequestError(
                "There was an error while fetching the delegations"
            )

        delegation_fields = []
        for delegation in delegations:
            delegation_fields.extend(
                [
                    {
                        "name": "Delegator Address",
                        "value": delegation["delegator_address"],
                    },
                    {
                        "name": "Shares",
                        "value": delegation["shares"],
                    },
                    {
                        "name": "Balance",
                        "value": delegation["balance"],
                    },
                ]
            )

        await pretty_print(
            ctx,
            delegation_fields,
            title=f"Delegations of {address}",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="block",
        help="Get a block at a certain height",
    )
    async def block(self, ctx, height: str = "latest"):
        block = block_api.get_block(height)
        if block is None:
            raise errors.RequestError("There was an error while fetching the block")

        await pretty_print(
            ctx,
            [
                {
                    "name": "Time (UTC)",
                    "value": block["time"],
                    "inline": False,
                },
                {
                    "name": "# Hash",
                    "value": block["hash"],
                    "inline": False,
                },
                {
                    "name": "No. of Txs",
                    "value": str(block["number_of_transactions"]),
                    "inline": False,
                },
                {
                    "name": "Proposer Moniker",
                    "value": block["proposer"]["moniker"],
                },
                {
                    "name": "Proposer Address",
                    "value": block["proposer"]["address"],
                },
            ],
            title=f"Block {block['height']}",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )
