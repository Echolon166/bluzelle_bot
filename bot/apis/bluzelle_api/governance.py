import re
import requests
import datetime

from apis import returnReqError
from constants import *


def get_proposals():
    """Get the list of all proposals

    Returns:
        List[dict]: A list of dicts which consists of following keys:
            id, title, status, submit_time, voting_start_time, total_deposit
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/gov/v1beta1/proposals"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    proposals = result.json()["proposals"]

    proposal_list = []
    for proposal in proposals:
        # Total deposited amount
        amount = int(float(proposal["total_deposit"][0]["amount"]) / BLZ_UBNT_RATIO)

        # Format status
        status = " ".join([t.capitalize() for t in proposal["status"].split("_")[2:]])

        # Format submit time
        submit_time = datetime.datetime.strptime(
            proposal["submit_time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
        )
        formatted_submit_time = submit_time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

        # Format voting start time
        voting_start_time = datetime.datetime.strptime(
            proposal["voting_start_time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
        )
        formatted_voting_start_time = voting_start_time.strftime(
            "%d %b %Y, %#I:%M:%S%p UTC"
        )

        proposal_list.append(
            {
                "id": proposal["proposal_id"],
                "title": proposal["content"]["title"],
                "status": status,
                "submit_time": formatted_submit_time,
                "voting_start_time": formatted_voting_start_time,
                "total_deposit": f"{amount} {BLZ_SYMBOL}",
            }
        )

    # Reverse in order to get latest proposal first
    proposal_list.reverse()

    return proposal_list


def get_proposal_by_id(id):
    """Get the list of all proposals

    Args:
        address (int): The id of the proposal

    Returns:
        dict: A dict which consists of following keys:
            id, proposer, title, description, type, final_tally_result, final_tally_result['yes'], final_tally_result['abstain'],
            final_tally_result['no'], final_tally_result['no_with_veto'], status, submit_time, deposit_end_time, voting_start_time,
            voting_end_time, total_deposit
    """

    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/gov/v1beta1/proposals/{id}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    proposal = result.json()["proposal"]

    # Ge proposer
    proposer = ""
    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/gov/proposals/{id}/proposer"
    result = requests.get(url)
    if result.status_code == 200:
        proposer = result.json()["result"]["proposer"]

    # Total deposited amount
    amount = int(float(proposal["total_deposit"][0]["amount"]) / BLZ_UBNT_RATIO)

    # Format type
    type = proposal["content"]["@type"].split(".")[-1]

    # Format status
    status = " ".join([t.capitalize() for t in proposal["status"].split("_")[2:]])

    # Format submit time
    submit_time = datetime.datetime.strptime(
        proposal["submit_time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
    )
    formatted_submit_time = submit_time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

    # Format deposit end time
    deposit_end_time = datetime.datetime.strptime(
        proposal["deposit_end_time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
    )
    formatted_deposit_end_time = deposit_end_time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

    # Format voting start time
    voting_start_time = datetime.datetime.strptime(
        proposal["voting_start_time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
    )
    formatted_voting_start_time = voting_start_time.strftime(
        "%d %b %Y, %#I:%M:%S%p UTC"
    )

    # Format voting end time
    voting_end_time = datetime.datetime.strptime(
        proposal["voting_end_time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
    )
    formatted_voting_end_time = voting_end_time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

    # Format final_tally_result fields
    yes_partition = str(
        float(proposal["final_tally_result"]["yes"]) / BLZ_UBNT_RATIO
    ).partition(".")
    yes_seperated = re.sub(r"(?<!^)(?=(\d{3})+$)", r",", yes_partition[0])

    abstain_partition = str(
        float(proposal["final_tally_result"]["abstain"]) / BLZ_UBNT_RATIO
    ).partition(".")
    abstain_seperated = re.sub(r"(?<!^)(?=(\d{3})+$)", r",", abstain_partition[0])

    no_partition = str(
        float(proposal["final_tally_result"]["no"]) / BLZ_UBNT_RATIO
    ).partition(".")
    no_seperated = re.sub(r"(?<!^)(?=(\d{3})+$)", r",", no_partition[0])

    no_with_veto_partition = str(
        float(proposal["final_tally_result"]["no_with_veto"]) / BLZ_UBNT_RATIO
    ).partition(".")
    no_with_veto_seperated = re.sub(
        r"(?<!^)(?=(\d{3})+$)", r",", no_with_veto_partition[0]
    )

    return {
        "id": proposal["proposal_id"],
        "proposer": proposer,
        "title": proposal["content"]["title"],
        "description": proposal["content"]["description"],
        "type": type,
        "final_tally_result": {
            "yes": f"{yes_seperated}{yes_partition[1]}{yes_partition[2]}",
            "abstain": f"{abstain_seperated}{abstain_partition[1]}{abstain_partition[2]}",
            "no": f"{no_seperated}{no_partition[1]}{no_partition[2]}",
            "no_with_veto": f"{no_with_veto_seperated}{no_with_veto_partition[1]}{no_with_veto_partition[2]}",
        },
        "status": status,
        "submit_time": formatted_submit_time,
        "deposit_end_time": formatted_deposit_end_time,
        "voting_start_time": formatted_voting_start_time,
        "voting_end_time": formatted_voting_end_time,
        "total_deposit": f"{amount} {BLZ_SYMBOL}",
    }
