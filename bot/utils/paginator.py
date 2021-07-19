import random
from asyncio import TimeoutError
from typing import Optional, Union

import discord
from discord.ext import commands

from discord_slash import SlashContext
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    create_actionrow,
    create_button,
    wait_for_component,
)


async def Paginator(
    bot: commands.bot,
    ctx: SlashContext,
    pages: list[discord.Embed],
    content: Optional[str] = None,
    previous_label: str = None,
    next_label: str = None,
    previous_emoji: Optional[
        Union[discord.emoji.Emoji, discord.partial_emoji.PartialEmoji, dict]
    ] = "⬅",
    next_emoji: Optional[
        Union[discord.emoji.Emoji, discord.partial_emoji.PartialEmoji, dict]
    ] = "➡",
    index_style: Optional[Union[ButtonStyle, int]] = 2,
    previous_style: Optional[Union[ButtonStyle, int]] = 2,
    next_style: Optional[Union[ButtonStyle, int]] = 2,
    timeout: Optional[int] = None,
):
    # Limit of the paginator
    top = len(pages)

    # Base of button id
    bid = random.randint(10000, 99999)

    # Starting page
    index = 0

    control_buttons = [
        # Previous Button
        create_button(
            style=previous_style,
            label=previous_label,
            custom_id=f"{bid}-prev",
            disabled=True,
            emoji=previous_emoji,
        ),
        # Index
        create_button(
            style=index_style,
            label=f"{index+1}/{top}",
            custom_id=f"{bid}-index",
            disabled=True,
        ),
        # Next Button
        create_button(
            style=next_style,
            label=next_label,
            custom_id=f"{bid}-next",
            disabled=False,
            emoji=next_emoji,
        ),
    ]

    controls = create_actionrow(*control_buttons)
    message = await ctx.send(
        content=content,
        embed=pages[0],
        components=[controls],
    )

    # Handling the interaction

    # Stop listening if the timeout expires
    tmt = True
    while tmt:
        try:
            button_context: ComponentContext = await wait_for_component(
                bot, components=[controls], timeout=timeout
            )
            await button_context.defer(edit_origin=True)
        except TimeoutError:
            tmt = False
            await message.edit(
                content=content,
                embed=pages[index],
                components=None,
            )

        else:
            # Handling the previous button
            if button_context.component_id == f"{bid}-prev" and index > 0:
                index -= 1
                if index == 0:
                    # Disable the previous button if index is 0
                    controls["components"][0]["disabled"] = True

                # Enable Next Button
                controls["components"][2]["disabled"] = False

                # Update the index
                controls["components"][1]["label"] = f"{index+1}/{top}"

                await button_context.edit_origin(
                    content=content,
                    embed=pages[index],
                    components=[controls],
                )

            # Handling the next button
            if button_context.component_id == f"{bid}-next" and index < top - 1:
                index += 1
                if index == top - 1:
                    # Disable the next button if index is the last page
                    controls["components"][2]["disabled"] = True

                # Enable Previous Button
                controls["components"][0]["disabled"] = False

                # Update the index
                controls["components"][1]["label"] = f"{index+1}/{top}"

                await button_context.edit_origin(
                    content=content,
                    embed=pages[index],
                    components=[controls],
                )
