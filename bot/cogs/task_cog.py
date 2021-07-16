import sys
import traceback
import threading
import asyncio
import time

from discord.ext import commands, tasks

import data
import errors
import validation
from cogs import channel_cog
from constants import *
from utils import pretty_print, requested_by_footer
from utils.mappings import get_mapping


class TaskCommands(commands.Cog):
    """
    Cog for processing task commands which are often only presented to administrators.
    """

    def __init__(self, bot):
        self.bot = bot
        self.task_run_lock = threading.Lock()
        self.run_tasks.start()

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
                        task_function = getattr(
                            channel_cog.ChannelCommands, task["function"]
                        )
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

    @commands.command(
        name="add_task",
        help="Add a new task which will be repeated per interval",
    )
    @validation.owner_or_permissions(administrator=True)
    async def add_task(
        self,
        ctx,
        channel: str,
        # Currently only supports seconds
        interval: int,
        function: str,
        *kwargs,
    ):
        # Get the channel id
        id = "".join(c for c in channel if c.isdigit())

        kwarg_mapping = get_mapping(function, kwargs)

        task = {
            "channel_id": id,
            "latest_execution": time.time(),
            "interval": interval,
            "kwargs": kwarg_mapping,
            "function": function,
        }

        # Call for the first time to test if there are any errors, doesn't add the task if there is any
        # Currently, only supports commands from channel_cog.ChannelCommands
        task_function = getattr(channel_cog.ChannelCommands, task["function"])

        channel_id = task["channel_id"]
        channel_obj = await self.bot.fetch_channel(channel_id)

        await task_function(self, channel_obj, **kwarg_mapping)

        data.add_task(task)

    @commands.command(
        name="delete_task",
        help="Delete task by id",
    )
    @validation.owner_or_permissions(administrator=True)
    async def delete_task(self, ctx, id: int):
        data.delete_task(id)

    @commands.command(
        name="tasks",
        help="Get the list of all active tasks",
    )
    @validation.owner_or_permissions(administrator=True)
    async def tasks(self, ctx):
        tasks = data.get_tasks()

        task_fields = []
        for task in tasks:
            parameters = ""
            for key, value in task["kwargs"].items():
                parameters += f"{key}: {value}\n"

            task_fields.extend(
                [
                    {
                        "name": "ID",
                        "value": task["id"],
                    },
                    {
                        "name": "Channel",
                        "value": f"<#{task['channel_id']}>",
                    },
                    {
                        "name": "Interval",
                        "value": f"{task['interval']} seconds",
                    },
                    {
                        "name": "Function",
                        "value": task["function"],
                        "inline": False,
                    },
                    {
                        "name": "Parameters",
                        "value": parameters,
                        "inline": False,
                    },
                ]
            )

        await pretty_print(
            ctx,
            task_fields,
            title="Active Tasks",
            footer=requested_by_footer(ctx),
            timestamp=True,
            color=WHITE_COLOR,
        )
