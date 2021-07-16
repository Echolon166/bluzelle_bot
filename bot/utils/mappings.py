def get_mapping(function, kwargs):
    """Command parameter mappings to be used by add_tasks function in order to invoke the command

    Args:
        function (str): Name of the function
        kwargs (List[String]): A list of strings to be mapped as parameters for the function

    Returns:
        dict: A dict of mapped parameters
    """

    if function == "price":
        return price_mapping(kwargs)
    elif function == "validator":
        return validator_mapping(kwargs)
    elif function == "delegations":
        return delegations_mapping(kwargs)
    return {}


# TODO: ADD PRICE MAPPING
def price_mapping(*kwargs):
    return {}


def validator_mapping(*kwargs):
    return {
        "address": kwargs[0][0],
    }


def delegations_mapping(*kwargs):
    return {
        "address": kwargs[0][0],
    }
