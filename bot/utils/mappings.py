from cogs import block_cog, economy_cog, transaction_cog, validator_cog


def get_parameter_mapping(function, kwargs):
    """Command parameter mappings to be used by add_tasks function in order to invoke the command

    Args:
        function (str): Name of the function
        kwargs (List[String]): A list of strings to be mapped as parameters for the function

    Returns:
        dict: A dict of mapped parameters
    """

    if function == "price":
        return price_parameter_mapping(kwargs)
    elif function == "validator":
        return validator_parameter_mapping(kwargs)
    elif function == "delegations":
        return delegations_parameter_mapping(kwargs)
    elif function == "transaction":
        return transaction_parameter_mapping(kwargs)
    return {}


# TODO: ADD PRICE MAPPING
def price_parameter_mapping(*kwargs):
    return {}


def validator_parameter_mapping(*kwargs):
    return {
        "address": kwargs[0][0],
    }


def delegations_parameter_mapping(*kwargs):
    return {
        "address": kwargs[0][0],
    }


def transaction_parameter_mapping(*kwargs):
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
