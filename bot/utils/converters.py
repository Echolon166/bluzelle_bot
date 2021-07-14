from discord.ext import commands

import errors
from apis import coingecko_api


class CryptoCoin(commands.Converter):
    """Converter to check if the given coin is valid, and if valid, return it's price data.

    Raises:
        errors.InvalidArgument: No coin exists with given symbol.
        errors.RequestError: There was an error while fetching the data.

    Returns:
        dict: A dict which consists of following keys:
            symbol and data(price data).
    """

    async def convert(self, ctx, argument):
        # Check if the coin is valid
        valid = coingecko_api.valid_coin(argument)
        if not valid:
            raise errors.InvalidArgument("Invalid coin symbol")

        # Retrieve the price data of the coin
        data = coingecko_api.get_price_data(argument)
        if data is None:
            raise errors.RequestError("There was an error while fetching the coin data")

        return {"symbol": argument.upper(), "data": data}
