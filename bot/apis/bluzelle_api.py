import requests
from bech32 import bech32_decode, bech32_encode

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

    pooled_tokens = get_pooled_tokens()
    if pooled_tokens["bonded_tokens"] is None:
        return None

    total_voting_power = int(pooled_tokens["bonded_tokens"]) / 1000000

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
    """Get the validator info of given operator address

    Args:
        address (str): Validator address

    Returns:
        dict: A dict which consists of following keys:
            moniker, identity, website, security_contact, details, tokens, delegator_shares, self_delegate_address, self_delegation_ratio, voting_power, voting_power_percentage, commission_rate, max_rate, max_change_rate
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators/{address}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validator = result.json()["validator"]

    pooled_tokens = get_pooled_tokens()
    if pooled_tokens["bonded_tokens"] is None:
        return None

    self_delegate_address = get_delegate_from_operator(address)

    self_delegation = get_validator_self_delegation(address, self_delegate_address)
    if self_delegation is None:
        return None

    total_voting_power = int(pooled_tokens["bonded_tokens"]) / 1000000
    voting_power = int(int(validator["tokens"]) / 1000000)

    return {
        "moniker": validator["description"]["moniker"],
        "identity": validator["description"]["identity"],
        "website": validator["description"]["website"],
        "security_contact": validator["description"]["security_contact"],
        "details": validator["description"]["details"],
        "tokens": validator["tokens"],
        "delegator_shares": f"{int(float(validator['delegator_shares']))}",
        "self_delegate_address": self_delegate_address,
        "self_delegation_ratio": f"{int(float(validator['delegator_shares']) / float(self_delegation['delegation']['shares']) * 100)}%",
        "voting_power": voting_power,
        "voting_power_percentage": f"{100 / total_voting_power * voting_power}%",
        "commission_rate": f"{int(float(validator['commission']['commission_rates']['rate']) * 100)}%",
        "max_rate": f"{int(float(validator['commission']['commission_rates']['max_rate']) * 100)}%",
        "max_change_rate": f"{int(float(validator['commission']['commission_rates']['max_change_rate']) * 100)}%",
    }


def get_validator_self_delegation(operator_address, self_delegate_address):
    """Get self delegation of given validator

    Args:
        operator_address (str): Operator address of validator
        self_delegate_address (str): Self delegate address of validator

    Returns:
        dict: A dict which consists of following keys:
            delegation, delegation['delegator_address'], delegation['validator_address'], delegation['shares'], balance, balance['denom'], balance['amount']
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators/{operator_address}/delegations/{self_delegate_address}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    return result.json()["delegation_response"]


def get_validator_delegations(operator_address):
    """Get delegations of given validator

    Args:
        operator_address (str): Operator address of validator

    Returns:
        List[dict]: A list of dicts which consists of following keys:
            delegator_address, shares, balance
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators/{operator_address}/delegations"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    delegations = result.json()["delegation_responses"]

    delegation_list = []
    for delegation in delegations:
        delegation_list.append(
            {
                "delegator_address": delegation["delegation"]["delegator_address"],
                "shares": int(float(delegation["delegation"]["shares"])),
                "balance": f"{int(delegation['balance']['amount']) / 1000000} BLZ",
            }
        )

    return delegation_list


def get_delegate_from_operator(operator_address):
    """Get self-delegate address from operator address

    Args:
        operator_address (str): Operator address of validator

    Returns:
        str: Self-delegate address of validator
    """

    address = bech32_decode(operator_address)

    return bech32_encode("bluzelle", address[1])


def get_pooled_tokens():
    """Get total number of pooled tokens

    Returns:
        dict: A dict which consists of following keys:
            not_bonded_tokens, bonded_tokens
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/pool"

    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    return result.json()["pool"]
