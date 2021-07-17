import sys
import traceback

from discord.ext import commands

import errors
from utils import pretty_print, requested_by_footer
from constants import *
from apis.bluzelle_api import block as block_api


class Block(commands.Cog):
    """
    Block related commands.
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
