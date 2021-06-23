import sys
import traceback

from discord.ext import commands

import errors


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
