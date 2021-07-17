import discord
from discord.ext import commands, tasks

import config
import data
from constants import *
from cogs import (
    block_cog,
    economy_cog,
    options_cog,
    validator_cog,
    transaction_cog,
    task_cog,
)


config.parse_args()
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
default_prefix = config.CONFIG.command_prefix


def prefix(bot, ctx):
    try:
        guildId = ctx.guild.id
        return data.get_prefix(guildId) or default_prefix
    except:
        return default_prefix


class RallyRoleBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=prefix,
            case_insensitive=True,
            intents=intents,
            chunk_guilds_at_startup=True,
        )

        self.add_cog(economy_cog.Economy(self))
        self.add_cog(block_cog.Block(self))
        self.add_cog(validator_cog.Validator(self))
        self.add_cog(task_cog.Task(self))
        self.add_cog(options_cog.Options(self))
        self.add_cog(transaction_cog.Transaction(self))

        data.delete_all_commands()
        for command in self.commands:
            data.add_command(command.name, command.help)

    async def close(self):
        await super().close()

    def run(self):
        super().run(config.CONFIG.secret_token, reconnect=True)


bot = RallyRoleBot()
if __name__ == "__main__":
    bot.run()
