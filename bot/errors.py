from discord.ext import commands
from discord.ext.commands import errors

from constants import *
from utils import pretty_print


class InvalidArgument(commands.CommandError):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message


class RequestError(commands.CommandError):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message


def standart_error_handler(error_function):
    """
    Decorator that is prepended to a cog_command_error.
    It transforms the error handler into one that makes helpful and specific checks
        and returns a function that readily prints the error.

    Args:
        error_function (discord.ext.commands.CommandError): [description]
    """

    async def wrapper(cls, ctx, error):

        extra = f"\n\nSee the help message for more information."

        # This prevents any commands with local handlers being handled here.
        if hasattr(ctx.command, "on_error"):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found, we keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        ignored = (commands.CommandNotFound,)

        # Anything in ignored will return and prevent anything happening.
        if any([isinstance(error, i) for i in ignored]):
            return

        if isinstance(error, errors.DisabledCommand):
            await pretty_print(
                ctx,
                "This command is disabled!",
                title="Error",
                color=ERROR_COLOR,
            )

        elif isinstance(error, errors.MemberNotFound):
            await pretty_print(
                ctx,
                str(error) + "\nNote: This command is case-sensitive." + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, errors.RoleNotFound):
            await pretty_print(
                ctx,
                str(error) + "\nNote: This command is case-sensitive." + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, errors.NoPrivateMessage):
            await pretty_print(
                ctx,
                "This command cannot be run in a private message." + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, errors.PrivateMessageOnly):
            try:
                await ctx.message.delete()
                extra += "\nYour message has been deleted"
            except:
                print("Could not delete message.")
            await pretty_print(
                ctx,
                "This command should be run in a Private Message only!" + extra,
                title="Error",
                color=ERROR_COLOR,
            )

        elif isinstance(error, errors.MissingRole):
            await pretty_print(
                ctx,
                str(error) + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, errors.CheckFailure):
            await pretty_print(
                ctx,
                "Could not run command, do you have sufficient permissions in this channel?"
                + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, errors.BadArgument):
            await ctx.send_help(ctx.command)
            await pretty_print(
                ctx,
                "Could not run command, is it formatted properly?" + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, errors.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            await pretty_print(
                ctx,
                "Missing required arguments.",
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, InvalidArgument):
            await pretty_print(
                ctx,
                error.message + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        elif isinstance(error, RequestError):
            await pretty_print(
                ctx,
                error.message + extra,
                title="Error",
                color=ERROR_COLOR,
            )
            return

        await error_function(cls, ctx, error)

    return wrapper
