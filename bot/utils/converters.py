from bech32 import bech32_decode
from discord.ext import commands


import errors
from apis import coingecko_api
import utils.mappings as mappings


class CryptoCoin(commands.Converter):
    """Converter to check if the given coin is valid.

    Raises:
        errors.InvalidArgument: No coin exists with given symbol.

    Returns:
        str: Symbol of the coin
    """

    async def convert(self, ctx, argument):
        # Check if the coin is valid
        valid = coingecko_api.valid_coin(argument)
        if not valid:
            raise errors.InvalidArgument("Invalid coin symbol")

        return argument.upper()


class AccountAddress(commands.Converter):
    """Converter to check if the account address is valid.

    Raises:
        errors.InvalidArgument: Invalid address format/prefix

    Returns:
        str: Address of the account
    """

    async def convert(self, ctx, argument):
        expected_prefix = "bluzelle"

        # Decode the address
        address = bech32_decode(argument)

        # Check if the address is valid
        if address[0] == None or address[1] == None:
            raise errors.InvalidArgument("Invalid address format")

        # Check if the address prefix is correct
        if address[0] != expected_prefix:
            raise errors.InvalidArgument(
                f"Invalid address prefix\n'{expected_prefix}' expected, '{address[0]}' found"
            )

        return argument


class ValidatorAddress(commands.Converter):
    """Converter to check if the validator address is valid.

    Raises:
        errors.InvalidArgument: Invalid address format/prefix

    Returns:
        str: Address of the account
    """

    async def convert(self, ctx, argument):
        expected_prefix = "bluzellevaloper"

        # Decode the address
        address = bech32_decode(argument)

        # Check if the address is valid
        if address[0] == None or address[1] == None:
            raise errors.InvalidArgument("Invalid address format")

        # Check if the address prefix is correct
        if address[0] != expected_prefix:
            raise errors.InvalidArgument(
                f"Invalid address prefix\n'{expected_prefix}' expected, '{address[0]}' found"
            )

        return argument


class ValidFunction(commands.Converter):
    """Converter to check if the given function exists.

    Raises:
        errors.InvalidArgument: No function exists with given name.

    Returns:
        Function: Function itself
    """

    async def convert(self, ctx, argument):
        # Check if the function is valid
        function = mappings.get_command_mapping(argument)
        if not function:
            raise errors.InvalidArgument(
                "Invalid function name. Please be sure to add '_' inbetween words.\nEx: validator_get_details"
            )

        return argument
