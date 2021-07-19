import json
import re
import datetime
import requests

from apis import returnReqError
from constants import *


def get_transaction(hash):
    url = f"{BLUZELLE_PRIVATE_TESTNET_URL}:{BLUZELLE_API_PORT}/cosmos/tx/v1beta1/txs/{hash}"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    transaction = result.json()

    transaction_fee = transaction["tx_response"]["tx"]["auth_info"]["fee"]["amount"][0]

    denom = "BLZ" if transaction_fee["denom"] == "ubnt" else transaction_fee["denom"]

    gas_used_seperated = re.sub(
        r"(?<!^)(?=(\d{3})+$)", r",", transaction["tx_response"]["gas_used"]
    )

    gas_wanted_seperated = re.sub(
        r"(?<!^)(?=(\d{3})+$)", r",", transaction["tx_response"]["gas_wanted"]
    )

    # Format transaction timestamp
    time = datetime.datetime.strptime(
        transaction["tx_response"]["timestamp"][:26], "%Y-%m-%dT%H:%M:%SZ"
    )
    formatted_time = time.strftime("%d %b %Y, %#I:%M:%S%p UTC")

    return {
        "hash": transaction["tx_response"]["txhash"],
        "height": transaction["tx_response"]["height"],
        "time": formatted_time,
        "gas": f"{gas_used_seperated} / {gas_wanted_seperated}",
        "fee": f"{float(transaction_fee['amount']) / BLZ_UBNT_RATIO} {denom}",
        "memo": transaction["tx_response"]["tx"]["body"]["memo"],
        "messages": json.dumps(
            transaction["tx_response"]["tx"]["body"]["messages"],
            indent=4,
        ),
    }
