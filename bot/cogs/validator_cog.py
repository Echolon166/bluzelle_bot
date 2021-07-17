import sys
import traceback

from discord.ext import commands

import errors
from utils import pretty_print, requested_by_footer
from constants import *
from apis.bluzelle_api import validator as validator_api


class Validator(commands.Cog):
    """
    Validator related commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @errors.standart_error_handler
    async def cog_command_error(self, ctx, error):
        """
        A special method that is called whenever an error is dispatched inside this cog.
        This is similar to on_command_error() except only applying to the commands inside this cog.

        Args:
            ctx (Context): The invocation context where the error happened.
            error (CommandError): The error that happened.
        """

        print(
            "Ignoring exception in command {}:".format(ctx.command),
            file=sys.stderr,
        )

        traceback.print_exception(
            type(error),
            error,
            error.__traceback__,
            file=sys.stderr,
        )

    @commands.command(
        name="validators",
        help="Get the list of all active validators",
    )
    async def validators(self, ctx):
        validators = validator_api.get_validators()
        if validators is None:
            raise errors.RequestError(
                "There was an error while fetching the validators"
            )

        active_validators = [
            d
            for d in validators
            if d["jailed"] == False and d["status"] == "BOND_STATUS_BONDED"
        ]

        validator_fields = []
        validator_fields.append(
            {
                "name": "Active Validators",
                "value": f"{len(active_validators)} out of {len(validators)} validators",
                "inline": False,
            },
        )
        for validator in active_validators:
            validator_fields.extend(
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
                ]
            )

        await pretty_print(
            ctx,
            validator_fields,
            title="Validators",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="validator",
        help="Get the info of given validator",
    )
    async def validator(self, ctx, address: str):
        validator = validator_api.get_validator_by_address(address)
        if validator is None:
            raise errors.RequestError("There was an error while fetching the validator")

        await pretty_print(
            ctx,
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
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="delegations",
        help="Get delegations of given validator",
    )
    async def delegations(self, ctx, address: str):
        delegations = validator_api.get_validator_delegations(address)
        if delegations is None:
            raise errors.RequestError(
                "There was an error while fetching the delegations"
            )

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
            delegation_fields,
            title=f"Delegations of {address}",
            footer=requested_by_footer(ctx)
            if isinstance(ctx, commands.context.Context)
            else {},
            timestamp=True,
            color=WHITE_COLOR,
        )
