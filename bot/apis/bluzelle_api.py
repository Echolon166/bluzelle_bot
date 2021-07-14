import requests

from constants import *


def returnReqError(url, result):
    """Handler for the request errors.

    Args:
        url (str): URL which the request was made.
        result (requests.models.Response): Response of the request.
    """

    print("Request error!")
    print(f"Url: {url}")
    print(f"Status Code: {result.status_code}")
    try:
        print(f"JSON result type: {type(result.json())}")
        print(result.json())
    except:
        pass


def get_validators():
    """Get the list of all active validators

    Returns:
        List[dict]: A list of dicts which consists of following keys:
            moniker, address, voting_power, voting_power_percentage
    """
    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED&jailed=false&pagination.limit=100&pagination.count_total=true"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validators = result.json()["validators"]

    total_voting_power = 0
    for validator in validators:
        total_voting_power += int(validator["tokens"]) / 1000000

    validator_list = []
    for validator in validators:
        validator_voting_power = int(int(validator["tokens"]) / 1000000)

        validator_list.append(
            {
                "moniker": validator["description"]["moniker"],
                "address": validator["operator_address"],
                "voting_power": validator_voting_power,
                "voting_power_percentage": f"{100 / total_voting_power * validator_voting_power}%",
            }
        )

    return validator_list


def get_validator(address):
    """Get the validator info of given address

    Args:
        address (str): Validator address

    Returns:
        dict: A dict which consists of following keys:
            moniker, identity, website, security_contact, details, tokens, delegator_shares, voting_power, voting_power_percentage, commission_rate, max_rate, max_change_rate
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED&jailed=false&pagination.limit=100&pagination.count_total=true"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validators = result.json()["validators"]

    validator_info = None
    total_voting_power = 0
    for validator in validators:
        validator_voting_power = int(int(validator["tokens"]) / 1000000)
        total_voting_power += validator_voting_power

        if validator["operator_address"] == address:
            validator_info = {
                "moniker": validator["description"]["moniker"],
                "identity": validator["description"]["identity"],
                "website": validator["description"]["website"],
                "security_contact": validator["description"]["security_contact"],
                "details": validator["description"]["details"],
                "tokens": validator["tokens"],
                "delegator_shares": f"{int(float(validator['delegator_shares']))}",
                "voting_power": validator_voting_power,
                "commission_rate": f"{int(float(validator['commission']['commission_rates']['rate']) * 100)}%",
                "max_rate": f"{int(float(validator['commission']['commission_rates']['max_rate']) * 100)}%",
                "max_change_rate": f"{int(float(validator['commission']['commission_rates']['max_change_rate']) * 100)}%",
            }

    if validator_info is not None:
        validator_info[
            "voting_power_percentage"
        ] = f"{100 / total_voting_power * int(validator_info['voting_power'])}%"

    return validator_info
