from discord_slash import SlashContext

import errors
from utils import pretty_embed, pretty_print, pretty_print_paginate
from constants import *
from apis.bluzelle_api import governance as governance_api


async def proposals(self, ctx: SlashContext):
    proposals = governance_api.get_proposals()
    if proposals is None:
        raise errors.RequestError("There was an error while fetching the proposals")

    if len(proposals) == 0:
        await pretty_print(
            ctx,
            pretty_embed(
                {},
                title="Proposals",
                timestamp=True,
                color=WHITE_COLOR,
            ),
        )
    else:
        proposal_embeds = []
        for proposal in proposals:
            proposal_embeds.append(
                pretty_embed(
                    [
                        {
                            "name": "Proposal ID",
                            "value": proposal["id"],
                        },
                        {
                            "name": "Status",
                            "value": proposal["status"],
                        },
                        {
                            "name": "Total Deposit",
                            "value": proposal["total_deposit"],
                        },
                        {
                            "name": "Title",
                            "value": proposal["title"],
                            "inline": False,
                        },
                        {
                            "name": "Submit Time (UTC)",
                            "value": proposal["submit_time"],
                        },
                        {
                            "name": "Voting Start Time (UTC)",
                            "value": proposal["voting_start_time"],
                        },
                    ],
                    title="Proposals",
                    timestamp=True,
                    color=WHITE_COLOR,
                ),
            )

        if len(proposals) == 1:
            await pretty_print(
                ctx,
                proposal_embeds,
            )
        else:
            await pretty_print_paginate(
                self.bot,
                ctx,
                proposal_embeds,
            )
