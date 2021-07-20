import io

from discord import File
from discord_slash import SlashContext

import errors
from utils.printer import pretty_embed, pretty_print, pretty_print_paginate
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


async def proposal(
    self,
    ctx: SlashContext,
    id,
):
    proposal = governance_api.get_proposal_by_id(id)
    if proposal is None:
        raise errors.RequestError("There was an error while fetching the proposal")

    proposal_fields = [
        {
            "name": "Proposer",
            "value": proposal["proposer"],
        },
        {
            "name": "Title",
            "value": proposal["title"],
            "inline": False,
        },
        {
            "name": "Proposal Type",
            "value": proposal["type"],
        },
        {
            "name": "Proposal Status",
            "value": proposal["status"],
        },
        {
            "name": "Deposit",
            "value": proposal["total_deposit"],
        },
        {
            "name": "Tally Result (final)",
            "value": f"Yes: {proposal['final_tally_result']['yes']}\nAbstain: {proposal['final_tally_result']['abstain']}\nNo: {proposal['final_tally_result']['no']}\nNo with Veto: {proposal['final_tally_result']['no_with_veto']}",
            "inline": False,
        },
        {
            "name": "Submit Time",
            "value": proposal["submit_time"],
        },
        {
            "name": "Deposit End Time",
            "value": proposal["deposit_end_time"],
        },
        {
            "name": "\u200b",
            "value": "\u200b",
        },
        {
            "name": "Voting Start Time",
            "value": proposal["voting_start_time"],
        },
        {
            "name": "End Voting Time",
            "value": proposal["voting_end_time"],
        },
        {
            "name": "\u200b",
            "value": "\u200b",
        },
    ]

    if len(proposal["description"]) <= 1018:
        proposal_fields.insert(
            2,
            {
                "name": "Description",
                "value": proposal["description"],
                "inline": False,
            },
        )

        await pretty_print(
            ctx,
            pretty_embed(
                proposal_fields,
                title=f"Proposal {proposal['id']}",
                timestamp=True,
                color=WHITE_COLOR,
            ),
        )
    else:
        proposal_fields.insert(
            2,
            {
                "name": "Description",
                "value": "⬇️ Too long to fit inside the embed. Written in the file below. ⬇️",
                "inline": False,
            },
        )

        await pretty_print(
            ctx,
            pretty_embed(
                proposal_fields,
                title=f"Proposal {proposal['id']}",
                timestamp=True,
                color=WHITE_COLOR,
            ),
        )

        # Send the proposal's description to the channel as a file
        await ctx.send(
            file=File(
                io.StringIO(proposal["description"]),
                "proposal_description.txt",
            )
        )


async def online_voting_power(self, ctx: SlashContext):
    online_voting_power = governance_api.get_online_voting_power()
    if online_voting_power is None:
        raise errors.RequestError(
            "There was an error while fetching the online voting power"
        )

    await pretty_print(
        ctx,
        pretty_embed(
            [
                {
                    "name": online_voting_power["voting_power"],
                    "value": f"{online_voting_power['supply_percentage']} from {online_voting_power['total_supply']}",
                    "inline": False,
                },
            ],
            title="Online Voting Power (Now)",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )
