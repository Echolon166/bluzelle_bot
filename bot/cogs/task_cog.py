import threading
import asyncio
import time

from discord import TextChannel
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from cogs.commands import ping_api

import data
import utils.converters as converters
import utils.mappings as mappings
import validation
from constants import *
import cogs.commands.task_commands as task_commands


class Task(commands.Cog):
    """
    Task scheduling commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self.task_run_lock = threading.Lock()
        self.run_tasks.start()

    @tasks.loop(seconds=RUN_TASKS_INTERVAL)
    async def run_tasks(self):
        """
        Checks active tasks every RUN_TASKS_INTERVAL
        If their interval is passed, executes the task and updates their latest_execution
        """

        await self.bot.wait_until_ready()

        with self.task_run_lock:
            all_tasks = data.get_tasks()
            for task in all_tasks:
                try:
                    current_time = time.time()
                    # If interval amount of time has passed since latest_execution, execute the function
                    if current_time >= int(task["latest_execution"]) + int(
                        task["interval"]
                    ):
                        # Get function object, kwargs and channel_id
                        task_function = mappings.get_command_mapping(task["function"])
                        kwargs = task["kwargs"]
                        channel_id = task["channel_id"]

                        # Fetch the channel
                        channel = await self.bot.fetch_channel(channel_id)

                        # Call the function
                        asyncio.create_task(task_function(self, channel, **kwargs))

                        # Update latest_execution of the task
                        task["latest_execution"] = current_time
                        data.update_task(task)
                except Exception as e:
                    print(e)

    @cog_ext.cog_subcommand(
        base="task",
        name="add",
        description="[ADMIN ONLY] Add a task which will be repeated per interval",
        options=[
            create_option(
                name="channel",
                description="The channel which the task should be added",
                option_type=SlashCommandOptionType.CHANNEL,
                required=True,
            ),
            create_option(
                name="interval",
                description="Task schedule interval",
                option_type=SlashCommandOptionType.INTEGER,
                required=True,
            ),
            create_option(
                name="function",
                description="Function to be added as task ('_' inbetween words)(Ex. validator_get_details)",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
            create_option(
                name="parameters",
                description="Parameters of the function",
                option_type=SlashCommandOptionType.STRING,
                required=False,
            ),
        ],
    )
    @validation.owner_or_permissions(administrator=True)
    async def add_task(
        self,
        ctx: SlashContext,
        channel: TextChannel,
        # Currently only supports seconds
        interval: int,
        function: converters.ValidFunction,
        parameters: str = None,
    ):
        await ping_api(ctx)

        function = await converters.ValidFunction.convert(self, ctx, function)
        kwarg_mapping = await mappings.get_parameter_mapping(
            self, ctx, function, parameters
        )

        await task_commands.add_task(
            self,
            ctx,
            channel,
            interval,
            function,
            kwarg_mapping,
        )

    @cog_ext.cog_subcommand(
        base="task",
        name="delete",
        description="[ADMIN ONLY] Delete task by id",
        options=[
            create_option(
                name="id",
                description="Id of the task",
                option_type=SlashCommandOptionType.INTEGER,
                required=True,
            ),
        ],
    )
    @validation.owner_or_permissions(administrator=True)
    async def delete_task(self, ctx: SlashContext, id: int):
        await ping_api(ctx)
        await task_commands.delete_task(self, ctx, id)

    @cog_ext.cog_subcommand(
        base="task",
        subcommand_group="get",
        name="all",
        description="[ADMIN ONLY] Get the list of all active tasks",
    )
    @validation.owner_or_permissions(administrator=True)
    async def tasks(self, ctx: SlashContext):
        await ping_api(ctx)
        await task_commands.tasks(self, ctx)


def setup(bot):
    bot.add_cog(Task(bot))
