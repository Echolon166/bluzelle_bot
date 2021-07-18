import sys
import traceback

import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand

import config
import errors
import data
from constants import *
import cogs


config.parse_args()
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
default_prefix = "/"


class RallyRoleBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=default_prefix,
            case_insensitive=True,
            intents=intents,
            chunk_guilds_at_startup=True,
        )

        self.remove_command("help")

        slash = SlashCommand(
            self,
            sync_commands=True,
            sync_on_cog_reload=True,
        )

        for cog in cogs.__all__:
            self.load_extension(f"cogs.{cog}")

    async def close(self):
        await super().close()

    @commands.Cog.listener()
    @errors.standart_error_handler
    async def on_slash_command_error(self, ctx, error):
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

    def run(self):
        super().run(config.CONFIG.secret_token, reconnect=True)


bot = RallyRoleBot()
if __name__ == "__main__":
    bot.run()
