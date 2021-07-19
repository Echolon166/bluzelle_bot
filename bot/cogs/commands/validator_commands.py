from discord_slash import SlashContext

import errors
from utils import pretty_embed, pretty_print, pretty_print_paginate
from constants import *
from apis.bluzelle_api import validator as validator_api


async def validators(self, ctx: SlashContext):
    pg_threshold = 7

    validators = validator_api.get_validators()
    if validators is None:
        raise errors.RequestError("There was an error while fetching the validators")

    active_validators = [
        d
        for d in validators
        if d["jailed"] == False and d["status"] == "BOND_STATUS_BONDED"
    ]

    await pretty_print(
        ctx,
        pretty_embed(
            [
                {
                    "name": "Active Validators",
                    "value": f"{len(active_validators)} out of {len(validators)} validators",
                    "inline": False,
                },
            ],
            title="Validators",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )

    validator_list = []
    if len(active_validators) <= pg_threshold:
        for validator in active_validators:
            validator_list.extend(
                [
                    {
                        "name": "Moniker",
                        "value": validator["moniker"],
                    },
                    {
                        "name": "Operator Address",
                        "value": validator["address"],
                    },
                    {
                        "name": "Voting Power",
                        "value": f"{validator['voting_power']} ({validator['voting_power_percentage']})",
                    },
                ],
            )

        await pretty_print(
            ctx,
            pretty_embed(
                validator_list,
                title="Validators",
                timestamp=True,
                color=WHITE_COLOR,
            ),
        )
    else:
        x = 0
        validator_embeds = []
        for validator in active_validators:
            validator_list.extend(
                [
                    {
                        "name": "Moniker",
                        "value": validator["moniker"],
                    },
                    {
                        "name": "Operator Address",
                        "value": validator["address"],
                    },
                    {
                        "name": "Voting Power",
                        "value": f"{validator['voting_power']} ({validator['voting_power_percentage']})",
                    },
                ],
            )

            if x % pg_threshold == pg_threshold - 1 or x == len(active_validators) - 1:
                validator_embeds.append(
                    pretty_embed(
                        validator_list,
                        title="Validators",
                        timestamp=True,
                        color=WHITE_COLOR,
                    ),
                )

                validator_list = []
            x += 1

        await pretty_print_paginate(
            self.bot,
            ctx,
            validator_embeds,
        )


async def validator(
    self,
    ctx: SlashContext,
    address,
):
    validator = validator_api.get_validator_by_address(address)
    if validator is None:
        raise errors.RequestError("There was an error while fetching the validator")

    await pretty_print(
        ctx,
        pretty_embed(
            [
                {
                    "name": "Self-Delegate Address",
                    "value": validator["self_delegate_address"],
                },
                {
                    "name": "Self Delegation Ratio",
                    "value": validator["self_delegation_ratio"],
                },
                {
                    "name": "Identity",
                    "value": validator["identity"],
                    "inline": False,
                },
                {
                    "name": "Website",
                    "value": validator["website"],
                    "inline": False,
                },
                {
                    "name": "Security Contact",
                    "value": validator["security_contact"],
                    "inline": False,
                },
                {
                    "name": "Details",
                    "value": validator["details"],
                    "inline": False,
                },
                {
                    "name": "Voting Power",
                    "value": f"{validator['voting_power']} ({validator['voting_power_percentage']})",
                },
                {
                    "name": "Tokens",
                    "value": validator["tokens"],
                },
                {
                    "name": "Delegator Shares",
                    "value": validator["delegator_shares"],
                },
                {
                    "name": "Commission Rate",
                    "value": validator["commission_rate"],
                },
                {
                    "name": "Max Rate",
                    "value": validator["max_rate"],
                },
                {
                    "name": "Max Change Rate",
                    "value": validator["max_change_rate"],
                },
                {
                    "name": "Proposer Priority",
                    "value": validator["proposer_priority"],
                },
                {
                    "name": "Uptime",
                    "value": validator["uptime"],
                },
                {
                    "name": "\u200b",
                    "value": "\u200b",
                },
            ],
            title=f"Info of '{validator['moniker']}'",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )


async def delegations(
    self,
    ctx: SlashContext,
    address,
):
    delegations = validator_api.get_validator_delegations(address)
    if delegations is None:
        raise errors.RequestError("There was an error while fetching the delegations")

    delegation_fields = []
    for delegation in delegations:
        delegation_fields.extend(
            [
                {
                    "name": "Delegator Address",
                    "value": delegation["delegator_address"],
                },
                {
                    "name": "Shares",
                    "value": delegation["shares"],
                },
                {
                    "name": "Balance",
                    "value": delegation["balance"],
                },
            ]
        )

    await pretty_print(
        ctx,
        pretty_embed(
            delegation_fields,
            title=f"Delegations of {address}",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )
