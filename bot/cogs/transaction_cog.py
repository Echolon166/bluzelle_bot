import io
import sys
import traceback

from discord import File
from discord.ext import commands

import errors
from utils import pretty_print, requested_by_footer
from constants import *
from apis.bluzelle_api import transactions as transaction_api


class Transaction(commands.Cog):
    """
    Transaction related commands.
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
        name="transaction",
        help="Get transaction details",
    )
    async def transaction(self, ctx, hash: str):
        transaction = transaction_api.get_transaction(hash)
        if transaction is None:
            raise errors.RequestError(
                "There was an error while fetching the transaction"
            )

        transaction_fields = [
            {
                "name": "Hash",
                "value": transaction["hash"],
                "inline": False,
            },
            {
                "name": "Height",
                "value": transaction["height"],
            },
            {
                "name": "Time (UTC)",
                "value": transaction["time"],
            },
            {
                "name": "Fee",
                "value": transaction["fee"],
                "inline": False,
            },
            {
                "name": "Gas (used / wanted)",
                "value": transaction["gas"],
                "inline": False,
            },
            {
                "name": "Memo",
                "value": transaction["memo"],
                "inline": False,
            },
        ]

        if len(transaction["messages"]) <= 1018:
            transaction_fields.append(
                {
                    "name": "Activities",
                    "value": f"```{transaction['messages']}```",
                    "inline": False,
                },
            )

            await pretty_print(
                ctx,
                transaction_fields,
                title="Transaction Information",
                footer=requested_by_footer(ctx)
                if isinstance(ctx, commands.context.Context)
                else {},
                timestamp=True,
                color=WHITE_COLOR,
            )
        else:
            transaction_fields.append(
                {
                    "name": "Activities",
                    "value": "⬇️ Too long to fit inside the embed. Written in the file below. ⬇️",
                    "inline": False,
                },
            )

            await pretty_print(
                ctx,
                transaction_fields,
                title="Transaction Information",
                footer=requested_by_footer(ctx)
                if isinstance(ctx, commands.context.Context)
                else {},
                timestamp=True,
                color=WHITE_COLOR,
            )

            # Send the transaction's messages to the channel as a file
            await ctx.send(
                file=File(
                    io.StringIO(transaction["messages"]),
                    "transaction_activities.txt",
                )
            )
