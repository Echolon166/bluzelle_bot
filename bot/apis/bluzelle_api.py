import requests
import datetime
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
    """Get the list of all validators

    Returns:
        List[dict]: A list of dicts which consists of following keys:
            moniker, address, pub_key, jailed, status, voting_power, voting_power_percentage
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validators = result.json()["validators"]

    # Get total pooled bonded tokens
    pooled_tokens = get_pooled_tokens()
    if pooled_tokens["bonded_tokens"] is None:
        return None

    total_voting_power = int(pooled_tokens["bonded_tokens"]) / BLZ_UBNT_RATIO

    validator_list = []
    for validator in validators:
        validator_voting_power = int(int(validator["tokens"]) / BLZ_UBNT_RATIO)

        validator_list.append(
            {
                "moniker": validator["description"]["moniker"],
                "address": validator["operator_address"],
                "pub_key": validator["consensus_pubkey"]["key"],
                "jailed": validator["jailed"],
                "status": validator["status"],
                "voting_power": validator_voting_power,
                "voting_power_percentage": f"{100 / total_voting_power * validator_voting_power}%",
            }
        )

    return validator_list


def get_validator_by_address(address):
    """Get the validator info of given operator address

    Args:
        address (str): Validator address

    Returns:
        dict: A dict which consists of following keys:
            moniker, identity, website, security_contact, details, tokens, delegator_shares, self_delegate_address, self_delegation_ratio,
            proposer_priority, voting_power, voting_power_percentage, commission_rate, max_rate, max_change_rate
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators/{address}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validator = result.json()["validator"]

    # Get total pooled bonded tokens
    pooled_tokens = get_pooled_tokens()
    if pooled_tokens["bonded_tokens"] is None:
        return None

    # Get self delegation info
    self_delegate_address = get_delegate_from_operator(address)
    self_delegation = get_validator_self_delegation(address, self_delegate_address)
    if self_delegation is None:
        return None

    # Get validator infos from rpc to get proposer priority
    validator_infos = get_rpc_validator_info()
    if validator_infos is None:
        return None

    for validator_info in validator_infos:
        if validator_info["pub_key"] == validator["consensus_pubkey"]["key"]:
            proposer_priority = validator_info["proposer_priority"]
            break

    total_voting_power = int(pooled_tokens["bonded_tokens"]) / BLZ_UBNT_RATIO
    voting_power = int(int(validator["tokens"]) / BLZ_UBNT_RATIO)

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
        "proposer_priority": proposer_priority,
        "voting_power": voting_power,
        "voting_power_percentage": f"{100 / total_voting_power * voting_power}%",
        "commission_rate": f"{int(float(validator['commission']['commission_rates']['rate']) * 100)}%",
        "max_rate": f"{int(float(validator['commission']['commission_rates']['max_rate']) * 100)}%",
        "max_change_rate": f"{int(float(validator['commission']['commission_rates']['max_change_rate']) * 100)}%",
    }


def get_validator_by_pub_key(pub_key):
    """Get validator with matching pub_key

    Args:
        pub_key (str): Public key of validator

    Returns:
        dict: A list of dicts which consists of following keys:
            moniker, address, pub_key, jailed, status, voting_power, voting_power_percentage
    """

    validators = get_validators()
    if validators is None:
        return None

    for validator in validators:
        if validator["pub_key"] == pub_key:
            return validator
    return None


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
                "balance": f"{int(delegation['balance']['amount']) / BLZ_UBNT_RATIO} {BLZ_SYMBOL}",
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


def get_rpc_validator_info():
    """Get rpc info of all validators

    Returns:
        List[dict]: A list of dicts which consists of following keys:
            address, pub_key, proposer_priority
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_RPC_PORT}/validators"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validator_infos = result.json()["result"]["validators"]

    validator_info_list = []
    for validator_info in validator_infos:
        validator_info_list.append(
            {
                "address": validator_info["address"],
                "pub_key": validator_info["pub_key"]["value"],
                "proposer_priority": validator_info["proposer_priority"],
            }
        )

    return validator_info_list


def get_block(height="latest"):
    """Get a block at a certain height

    Args:
        height (str, optional): Height of the block. Defaults to "latest".

    Returns:
        dict: A dict which consists of following keys:
            height, hash, proposer, proposer['moniker'], proposer['address'], number_of_transactions, time
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/blocks"
    if height == "latest":
        url += f"/latest"
    else:
        url += f"/{height}"

    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    block = result.json()

    # Get validator infos from rpc to get associated pub_key of hashed address
    validator_infos = get_rpc_validator_info()
    if validator_infos is None:
        return None

    for validator_info in validator_infos:
        if validator_info["address"] == block["block"]["header"]["proposer_address"]:
            pub_key = validator_info["pub_key"]
            break

    # Get validator wih matcing pub_key
    validator = get_validator_by_pub_key(pub_key)
    if validator is None:
        return None

    # Format block time
    time = datetime.datetime.strptime(
        block["block"]["header"]["time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
    )
    formattedTime = time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

    return {
        "height": block["block"]["header"]["height"],
        "hash": block["block_id"]["hash"],
        "proposer": {
            "moniker": validator["moniker"],
            "address": validator["address"],
        },
        "number_of_transactions": len(block["block"]["data"]["txs"]),
        "time": formattedTime,
    }
