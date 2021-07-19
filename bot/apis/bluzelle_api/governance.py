import requests
import datetime
import json

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
        amount = int(float(proposal["total_deposit"][0]["amount"]) / BLZ_UBNT_RATIO)

        # Format status
        status = " ".join([t.capitalize() for t in proposal["status"].split("_")[2:]])

        # Format submit time
        submit_time = datetime.datetime.strptime(
            proposal["submit_time"][:26], "%Y-%m-%dT%H:%M:%S.%f"
        )
        formatted_submit_time = submit_time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

        # Format submit time
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
