import datetime

from discord import Embed, Color
from discord.ext import commands

from discord_slash.context import SlashContext

from utils.ext import *
from utils.paginator import Paginator


def pretty_embed(
    fields,
    thumbnail="",
    title="",
    footer={},
    timestamp=False,
    color=Color(0xFFFFFF),
):
    """A method for creating a custom embed.

    Args:
        fields (list or string): Either a comma separated list of fields(as dicts) or a single string.
            Each field is organized by [title, value, inline] as specified in Discord documentation.
        thumbnail (string): URL of the thumbnail.
        title (string): Title listed at the top of the embed.
        footer (dict): Footer dict with either of [text, icon_url] as key together with it's value.
        timestamp (bool): A bool to decide should the timestamp be added to the end of the Embed.
        color (string): A Hexadecimal code representing the color strip on the left side of the Embed.

    Returns:
        discord.Embed: Custom embed object.
    """

    # Create the embed, add timestamp to the end if requested
    if timestamp:
        embed = Embed(
            title=title,
            color=color,
            timestamp=datetime.datetime.utcnow(),
        )
    else:
        embed = Embed(
            title=title,
            color=color,
        )

    if type(fields) == list:
        for field in fields:
            # Add inline field as True if not specified
            if len(field) < 3:
                field["inline"] = True

            embed.add_field(
                name=field["name"],
                value=field["value"] if field["value"] else "\u200b",
                inline=field["inline"],
            )
    elif type(fields) == str:
        embed.add_field(
            name="\u200b",
            value=fields,
        )

    # Add text and/or icon as footer if requested
    if "text" in footer and "icon_url" in footer:
        embed.set_footer(text=footer["text"], icon_url=footer["icon_url"])
    elif "text" in footer:
        embed.set_footer(text=footer["text"]),
    elif "icon_url" in footer:
        embed.set_footer(icon_url=footer["icon_url"])

    # Add thumbnail if requested
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    return embed


async def pretty_print(
    ctx: SlashContext,
    embed: Embed,
    caption="",
):
    """A method for printing to the Discord channel with a custom embed.

    Args:
        ctx (discord.Context): The invocation context where the call was made.
        embed (discord.Embed): Embed to be printed.
        caption (string): A message to append to the top of the embed, useful for printing mentions and such.

    Returns:
        discord.message.Message: Message object itself.
    """

    if not ctx:
        return

    # Send the embed, add caption as content if requested
    if caption:
        message = await ctx.send(content=caption, embed=embed)
    else:
        message = await ctx.send(embed=embed)

    return message


async def pretty_print_paginate(
    bot: commands.bot,
    ctx: SlashContext,
    embeds: list[Embed],
    timeout=20,
    caption="",
):
    # Send the paginated embed, add caption as content if requested
    if caption:
        message = await Paginator(
            bot,
            ctx,
            pages=embeds,
            timeout=timeout,
        )
    else:
        message = await Paginator(
            bot,
            ctx,
            pages=embeds,
            content=caption,
            timeout=timeout,
        )
