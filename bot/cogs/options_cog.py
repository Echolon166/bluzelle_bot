import sys
import traceback

from discord.ext import commands

import data
import errors
import validation
from constants import *
from utils import pretty_print


class OptionsCommands(commands.Cog):
    """
    Cog for processing option commands which are often only presented to administrators.
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_after_invoke(self, ctx):
        """
        A special method that is called whenever an command is successfully called inside this cog.
        """
        await pretty_print(
            ctx,
            "Command completed successfully!",
            title="Success",
            color=SUCCESS_COLOR,
        )
        pass

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
        name="set_prefix",
        help="Prefix for bot commands",
    )
    @validation.owner_or_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):
        data.add_prefix_mapping(ctx.guild.id, prefix)
