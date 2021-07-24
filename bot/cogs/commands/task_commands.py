import time

from discord import TextChannel
from discord_slash import SlashContext

from utils.printer import pretty_embed, pretty_print, pretty_print_paginate
from constants import *
import errors
import utils.mappings as mappings
import utils.task_manager as task_manager


async def add_task(
    self,
    ctx: SlashContext,
    channel: TextChannel,
    # Currently only supports seconds
    interval: int,
    function,
    kwargs=None,
):
    task = task_manager.task(channel.id, time.time(), interval, kwargs, function)

    # Call for the first time to test if there are any errors, doesn't add the task if there is any
    task_function = mappings.get_command_mapping(task.function)

    await task_function(self, channel, **kwargs)

    task_manager.add_task(task)

    await pretty_print(
        ctx,
        pretty_embed(
            {},
            title=f"Task:'{function}' added successfully.",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )


async def delete_task(
    self,
    ctx: SlashContext,
    id: int,
):
    result = task_manager.delete_task(id)
    if result is False:
        raise errors.InvalidArgument(f"Task with id:{id} not found.")

    await pretty_print(
        ctx,
        pretty_embed(
            {},
            title=f"Task:'{id}' deleted successfully.",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )


async def tasks(self, ctx: SlashContext):
    pg_threshold = 3

    tasks = task_manager.get_tasks()

    task_list = []
    if len(tasks) <= pg_threshold:
        for task in tasks:
            parameters = ""
            for key, value in task.kwargs.items():
                parameters += f"{key}: {value}\n"

            task_list.extend(
                [
                    {
                        "name": "ID",
                        "value": str(task.id),
                    },
                    {
                        "name": "Channel",
                        "value": f"<#{task.channel_id}>",
                    },
                    {
                        "name": "Interval",
                        "value": f"{task.interval} seconds",
                    },
                    {
                        "name": "Function",
                        "value": task.function,
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
            pretty_embed(
                task_list,
                title="Active Tasks",
                timestamp=True,
                color=WHITE_COLOR,
            ),
        )
    else:
        x = 0
        task_embeds = []
        for task in tasks:
            parameters = ""
            for key, value in task["kwargs"].items():
                parameters += f"{key}: {value}\n"

            task_list.extend(
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

            if x % pg_threshold == pg_threshold - 1 or x == len(tasks) - 1:
                task_embeds.append(
                    pretty_embed(
                        task_list,
                        title="Active Tasks",
                        timestamp=True,
                        color=WHITE_COLOR,
                    ),
                )

                task_list = []
            x += 1

        await pretty_print_paginate(
            self.bot,
            ctx,
            task_embeds,
        )
