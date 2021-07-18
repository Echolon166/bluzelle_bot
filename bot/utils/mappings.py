from apis import coingecko_api
from cogs import block_cog, economy_cog, transaction_cog, validator_cog
from utils.converters import AccountAddress, CryptoCoin, ValidatorAddress


async def get_parameter_mapping(self, ctx, function, kwargs):
    """Command parameter mappings to be used by add_tasks function in order to invoke the command

    Args:
        function (str): Name of the function
        kwargs (List[String]): A list of strings to be mapped as parameters for the function

    Returns:
        dict: A dict of mapped parameters
    """

    if kwargs:
        # Functions with default parameters
        # If kwargs is empty, return {} to use default parameters, if not, return the mapped parameters
        if function == "price":
            return await price_parameter_mapping(self, ctx, kwargs)
        elif function == "block":
            return await block_parameter_mapping(self, ctx, kwargs)
    else:
        # If kwargs is empty, create an empty kwargs and return back empty values to raise error
        kwargs = {}
        kwargs[0] = {}

    # Functions without default parameters
    if function == "validator":
        return await validator_parameter_mapping(self, ctx, kwargs)
    elif function == "delegations":
        return await delegations_parameter_mapping(self, ctx, kwargs)
    elif function == "transaction":
        return await transaction_parameter_mapping(self, ctx, kwargs)
    elif function == "balance":
        return await balance_parameter_mapping(self, ctx, kwargs)

    return {}


async def price_parameter_mapping(self, ctx, *kwargs):
    return {
        "coin": await CryptoCoin.convert(self, ctx, kwargs[0][0]),
    }


async def validator_parameter_mapping(self, ctx, *kwargs):
    return {
        "address": await ValidatorAddress.convert(self, ctx, kwargs[0][0]),
    }


async def delegations_parameter_mapping(self, ctx, *kwargs):
    return {
        "address": await ValidatorAddress.convert(self, ctx, kwargs[0][0]),
    }


async def balance_parameter_mapping(self, ctx, *kwargs):
    return {
        "address": await AccountAddress.convert(self, ctx, kwargs[0][0]),
    }


async def block_parameter_mapping(self, ctx, *kwargs):
    return {
        "height": kwargs[0][0],
    }


async def transaction_parameter_mapping(self, ctx, *kwargs):
    return {
        "hash": kwargs[0][0],
    }


def get_command_mapping(function):
    """Command mappings to be used by task functions in order to invoke the command

    Args:
        function (str): Name of the function

    Returns:
        dict: A dict of mapped parameters
    """

    if function == "block":
        return getattr(block_cog.Block, function)
    elif function == "balance":
        return getattr(economy_cog.Economy, function)
    elif function == "community_pool":
        return getattr(economy_cog.Economy, function)
    elif function == "inflation":
        return getattr(economy_cog.Economy, function)
    elif function == "price":
        return getattr(economy_cog.Economy, function)
    elif function == "delegations":
        return getattr(validator_cog.Validator, function)
    elif function == "validator":
        return getattr(validator_cog.Validator, function)
    elif function == "validators":
        return getattr(validator_cog.Validator, function)
    elif function == "transaction":
        return getattr(transaction_cog.Transaction, function)
    return {}
