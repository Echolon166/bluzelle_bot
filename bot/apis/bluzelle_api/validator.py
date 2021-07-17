from bech32 import bech32_decode, bech32_encode
import requests

from apis import returnReqError
from apis.bluzelle_api.economy import get_pooled_tokens
from constants import *


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
            proposer_priority, voting_power, voting_power_percentage, commission_rate, max_rate, max_change_rate, uptime
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
    self_delegation = get_validator_delegation_by_address(
        address,
        self_delegate_address,
    )
    if self_delegation is None:
        return None

    # Get validator uptime
    uptime = get_validator_uptime(validator["consensus_pubkey"]["key"])
    if uptime is None:
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
        "uptime": uptime,
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


def get_valcons_address_by_pub_key(pub_key):
    """Get validator valcons address with matching pub_key

    Args:
        pub_key (str): Public key of validator

    Returns:
        str: Validator valcons address
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/validatorsets/latest"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validators = result.json()["result"]["validators"]

    for validator in validators:
        if validator["pub_key"]["value"] == pub_key:
            return validator["address"]
    return None


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


def get_validator_delegation_by_address(operator_address, delegator_address):
    """Get delegation of given validator by address

    Args:
        operator_address (str): Operator address of validator
        delegator_address (str): Address of delegator

    Returns:
        dict: A dict which consists of following keys:
            delegation, delegation['delegator_address'], delegation['validator_address'], delegation['shares'], balance, balance['denom'], balance['amount']
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/staking/v1beta1/validators/{operator_address}/delegations/{delegator_address}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    return result.json()["delegation_response"]


def get_delegate_from_operator(operator_address):
    """Get self-delegate address from operator address

    Args:
        operator_address (str): Operator address of validator

    Returns:
        str: Self-delegate address of validator
    """

    address = bech32_decode(operator_address)

    return bech32_encode("bluzelle", address[1])


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


def get_validator_uptime(pub_key):
    """Get uptime of the validator

    Args:
        pub_key (str): Public key of validator

    Returns:
        str: Uptime percentage of the validator
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/slashing/v1beta1/params"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    validator_params = result.json()["params"]

    valcons_address = get_valcons_address_by_pub_key(pub_key)
    if valcons_address is None:
        return None

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/slashing/v1beta1/signing_infos/{valcons_address}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    signing_info = result.json()["val_signing_info"]

    uptime = int(
        (
            int(validator_params["signed_blocks_window"])
            - int(signing_info["missed_blocks_counter"])
        )
        / int(validator_params["signed_blocks_window"])
        * 100
    )

    return f"{uptime}%"
