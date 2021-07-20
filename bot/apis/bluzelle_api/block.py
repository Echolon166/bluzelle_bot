import datetime
import requests

from apis import returnReqError
from apis.bluzelle_api.validator import get_rpc_validator_info, get_validator_by_pub_key
from constants import *


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
    formatted_time = time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

    return {
        "height": block["block"]["header"]["height"],
        "hash": block["block_id"]["hash"],
        "proposer": {
            "moniker": validator["moniker"],
            "address": validator["address"],
        },
        "number_of_transactions": len(block["block"]["data"]["txs"]),
        "time": formatted_time,
    }


def consensus_state():
    """Get consensus state

    Returns:
        dict: A dict which consists of following keys:
            height, round, setp, proposer, proposer['moniker'], proposer['address'], voting_power
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_RPC_PORT}/dump_consensus_state"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)

    consensus_state = result.json()["result"]["round_state"]

    # Get validator wih matcing pub_key
    validator = get_validator_by_pub_key(
        consensus_state["validators"]["proposer"]["pub_key"]["value"]
    )
    if validator is None:
        return None

    # Get voting power
    consensus_round = consensus_state["round"]
    consensus_votes = consensus_state["votes"][consensus_round]["prevotes_bit_array"]
    voting_power = round(float(consensus_votes.split(" ")[3]) * 100.0)

    return {
        "height": consensus_state["height"],
        "round": str(consensus_round),
        "step": str(consensus_state["step"]),
        "proposer": {
            "moniker": validator["moniker"],
            "address": validator["address"],
        },
        "voting_power": str(voting_power),
    }
