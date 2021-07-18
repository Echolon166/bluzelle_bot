from discord_slash import SlashContext

import errors
from utils import pretty_print
from constants import *
from apis.bluzelle_api import block as block_api


async def block(self, ctx: SlashContext, height: str = "latest"):
    block = block_api.get_block(height)
    if block is None:
        raise errors.RequestError("There was an error while fetching the block")

    await pretty_print(
        ctx,
        [
            {
                "name": "Time (UTC)",
                "value": block["time"],
                "inline": False,
            },
            {
                "name": "# Hash",
                "value": block["hash"],
                "inline": False,
            },
            {
                "name": "No. of Txs",
                "value": str(block["number_of_transactions"]),
                "inline": False,
            },
            {
                "name": "Proposer Moniker",
                "value": block["proposer"]["moniker"],
            },
            {
                "name": "Proposer Address",
                "value": block["proposer"]["address"],
            },
        ],
        title=f"Block {block['height']}",
        timestamp=True,
        color=WHITE_COLOR,
    )
