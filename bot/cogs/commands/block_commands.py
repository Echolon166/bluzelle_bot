from discord_slash import SlashContext

import errors
from utils import pretty_embed, pretty_print
from constants import *
from apis.bluzelle_api import block as block_api


async def block(self, ctx: SlashContext, height: str = "latest"):
    block = block_api.get_block(height)
    if block is None:
        raise errors.RequestError("There was an error while fetching the block")

    await pretty_print(
        ctx,
        pretty_embed(
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
        ),
    )


async def consensus_state(self, ctx: SlashContext):
    consensus_state = block_api.consensus_state()
    if consensus_state is None:
        raise errors.RequestError(
            "There was an error while fetching the consensus state"
        )

    await pretty_print(
        ctx,
        pretty_embed(
            [
                {
                    "name": "Height",
                    "value": consensus_state["height"],
                    "inline": False,
                },
                {
                    "name": "Round",
                    "value": consensus_state["round"],
                },
                {
                    "name": "Step",
                    "value": consensus_state["step"],
                },
                {
                    "name": "Proposer",
                    "value": consensus_state["proposer"]["moniker"],
                    "inline": False,
                },
                {
                    "name": "Voting Power",
                    "value": consensus_state["voting_power"],
                    "inline": False,
                },
            ],
            title="Consensus State",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )
