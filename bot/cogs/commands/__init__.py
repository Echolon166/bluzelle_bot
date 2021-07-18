from discord_slash import SlashContext


async def ping_api(ctx: SlashContext):
    """
    Pings the bot's API to extend interaction time from 3 seconds to 15 minutes.
    If not pinged, "Invalid interaction application command" error will be raised if
    interaction takes more than 3 seconds.
    """
    await ctx.defer()
