from discord.enums import Enum
from discord.ext.commands.bot import Bot
from cogs.commands import (
    block_commands,
    economy_commands,
    transaction_commands,
    validator_commands,
    task_commands,
)
import utils.converters as converters


class BotFunctions(str, Enum):
    block = "block"
    balance = "balance"
    community_pool = "community_pool"
    inflation = "inflation"
    price = "price"
    delegations = "validator_get_delegations"
    validator = "validator_get_details"
    validators = "validator_get_all"
    transaction = "transaction"
    add_task = "task_add"
    delete_task = "task_delete"
    tasks = "task_get_all"


async def get_parameter_mapping(self, ctx, function, kwargs):
    """Command parameter mappings to be used by add_tasks function in order to invoke the command

    Args:
        function (str): Name of the function
        kwargs (str):A string to be mapped as parameters for the function

    Returns:
        dict: A dict of mapped parameters
    """

    if kwargs:
        kwargs = kwargs.split(" ")
        # Functions with default parameters
        # If kwargs is empty, return {} to use default parameters, if not, return the mapped parameters
        if function == BotFunctions.price.value:
            return await price_parameter_mapping(self, ctx, kwargs[0])
        elif function == BotFunctions.block.value:
            return await block_parameter_mapping(self, ctx, kwargs[0])
    else:
        # If kwargs is empty, create an empty kwargs and return back empty values to raise error
        kwargs = ["", "", ""]

    # Functions without default parameters
    if function == BotFunctions.validator.value:
        return await validator_parameter_mapping(self, ctx, kwargs[0])
    elif function == BotFunctions.delegations.value:
        return await delegations_parameter_mapping(self, ctx, kwargs[0])
    elif function == BotFunctions.transaction.value:
        return await transaction_parameter_mapping(self, ctx, kwargs[0])
    elif function == BotFunctions.balance.value:
        return await balance_parameter_mapping(self, ctx, kwargs[0])

    return {}


async def price_parameter_mapping(self, ctx, coin):
    return {
        "coin": await converters.CryptoCoin.convert(self, ctx, coin),
    }


async def validator_parameter_mapping(self, ctx, address):
    return {
        "address": await converters.ValidatorAddress.convert(self, ctx, address),
    }


async def delegations_parameter_mapping(self, ctx, address):
    return {
        "address": await converters.ValidatorAddress.convert(self, ctx, address),
    }


async def balance_parameter_mapping(self, ctx, address):
    return {
        "address": await converters.AccountAddress.convert(self, ctx, address),
    }


async def block_parameter_mapping(self, ctx, height):
    return {
        "height": height,
    }


async def transaction_parameter_mapping(self, ctx, hash):
    return {
        "hash": hash,
    }


def get_command_mapping(function):
    """Command mappings to be used by task functions in order to invoke the command

    Args:
        function (str): Name of the function

    Returns:
        Function: Function itself
    """

    if function == BotFunctions.block.value:
        return getattr(block_commands, BotFunctions.block.name)
    elif function == BotFunctions.balance.value:
        return getattr(economy_commands, BotFunctions.balance.name)
    elif function == BotFunctions.community_pool.value:
        return getattr(economy_commands, BotFunctions.community_pool.name)
    elif function == BotFunctions.inflation.value:
        return getattr(economy_commands, BotFunctions.inflation.name)
    elif function == BotFunctions.price.value:
        return getattr(economy_commands, BotFunctions.price.name)
    elif function == BotFunctions.delegations.value:
        return getattr(validator_commands, BotFunctions.delegations.name)
    elif function == BotFunctions.validators.value:
        return getattr(validator_commands, BotFunctions.validators.name)
    elif function == BotFunctions.validator.value:
        return getattr(validator_commands, BotFunctions.validator.name)
    elif function == BotFunctions.transaction.value:
        return getattr(transaction_commands, BotFunctions.transaction.name)
    elif function == BotFunctions.add_task.value:
        return getattr(task_commands, BotFunctions.add_task.name)
    elif function == BotFunctions.delete_task.value:
        return getattr(task_commands, BotFunctions.delete_task.name)
    elif function == BotFunctions.tasks.value:
        return getattr(task_commands, BotFunctions.tasks.name)
    return {}
