import io

from discord import File
from discord_slash import SlashContext

import errors
from utils import pretty_embed, pretty_print
from constants import *
from apis.bluzelle_api import transaction as transaction_api


async def transaction(self, ctx: SlashContext, hash: str):
    transaction = transaction_api.get_transaction(hash)
    if transaction is None:
        raise errors.RequestError("There was an error while fetching the transaction")

    transaction_fields = [
        {
            "name": "Hash",
            "value": transaction["hash"],
            "inline": False,
        },
        {
            "name": "Height",
            "value": transaction["height"],
        },
        {
            "name": "Time (UTC)",
            "value": transaction["time"],
        },
        {
            "name": "Fee",
            "value": transaction["fee"],
            "inline": False,
        },
        {
            "name": "Gas (used / wanted)",
            "value": transaction["gas"],
            "inline": False,
        },
        {
            "name": "Memo",
            "value": transaction["memo"],
            "inline": False,
        },
    ]

    if len(transaction["messages"]) <= 1018:
        transaction_fields.append(
            {
                "name": "Activities",
                "value": f"```{transaction['messages']}```",
                "inline": False,
            },
        )

        await pretty_print(
            ctx,
            pretty_embed(
                transaction_fields,
                title="Transaction Information",
                timestamp=True,
                color=WHITE_COLOR,
            ),
        )
    else:
        transaction_fields.append(
            {
                "name": "Activities",
                "value": "⬇️ Too long to fit inside the embed. Written in the file below. ⬇️",
                "inline": False,
            },
        )

        await pretty_print(
            ctx,
            pretty_embed(
                transaction_fields,
                title="Transaction Information",
                timestamp=True,
                color=WHITE_COLOR,
            ),
        )

        # Send the transaction's messages to the channel as a file
        await ctx.send(
            file=File(
                io.StringIO(transaction["messages"]),
                "transaction_activities.txt",
            )
        )
