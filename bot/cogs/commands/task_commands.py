import time

from discord import TextChannel
from discord_slash import SlashContext

import data
from utils import pretty_embed, pretty_print, pretty_print_paginate
from constants import *
import utils.mappings as mappings


async def add_task(
    self,
    ctx: SlashContext,
    channel: TextChannel,
    # Currently only supports seconds
    interval: int,
    function,
    kwargs=None,
):
    task = {
        "channel_id": channel.id,
        "latest_execution": time.time(),
        "interval": interval,
        "kwargs": kwargs,
        "function": function,
    }

    # Call for the first time to test if there are any errors, doesn't add the task if there is any
    task_function = mappings.get_command_mapping(task["function"])

    await task_function(self, channel, **kwargs)

    data.add_task(task)

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
    data.delete_task(id)

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

    tasks = data.get_tasks()

    task_list = []
    if len(tasks) <= pg_threshold:
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
