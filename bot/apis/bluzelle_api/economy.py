import re
import requests

from apis import returnReqError
from constants import *


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


def get_inflation():
    """Get inflation rate

    Returns:
        str: Inflation rate
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/mint/v1beta1/inflation"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    inflation = float(result.json()["inflation"])

    return f"{'{:.2f}'.format(inflation)}%"


def get_balances(address):
    """Get balances of an address

    Args:
        address (str): Account address

    Returns:
        List[dict]: A list of dicts which consists of following keys:
            denom, amount
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/bank/balances/{address}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    balances = result.json()["result"]

    balance_list = []
    for balance in balances:
        denom = "BLZ" if balance["denom"] == "ubnt" else balance["denom"]

        amount_partition = str(float(balance["amount"]) / BLZ_UBNT_RATIO).partition(".")
        amount_seperated = re.sub(r"(?<!^)(?=(\d{3})+$)", r",", amount_partition[0])

        balance_list.append(
            {
                "denom": denom,
                "amount": f"{amount_seperated}{amount_partition[1]}{amount_partition[2]}",
            }
        )

    return balance_list


def get_community_pools():
    """Get community pool coins

    Returns:
        List[dict]: A list of dicts which consists of following keys:
            denom, amount
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/distribution/v1beta1/community_pool"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    pools = result.json()["pool"]

    pool_list = []
    for pool in pools:
        denom = "BLZ" if pool["denom"] == "ubnt" else pool["denom"]

        amount_partition = str(float(pool["amount"]) / BLZ_UBNT_RATIO).partition(".")
        amount_seperated = re.sub(r"(?<!^)(?=(\d{3})+$)", r",", amount_partition[0])

        pool_list.append(
            {
                "denom": denom,
                "amount": f"{amount_seperated}{amount_partition[1]}{amount_partition[2]}",
            }
        )

    return pool_list
