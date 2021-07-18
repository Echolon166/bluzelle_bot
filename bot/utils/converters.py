from bech32 import bech32_decode
from discord.ext import commands


import errors
from apis import coingecko_api


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
