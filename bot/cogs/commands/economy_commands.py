from discord_slash import SlashContext

import errors
from utils.printer import pretty_embed, pretty_print
from constants import *
from apis import coingecko_api
from apis.bluzelle_api import economy as economy_api


async def price(
    self,
    ctx: SlashContext,
    coin: str = "BLZ",
):
    # Retrieve the price data of the coin
    data = coingecko_api.get_price_data(coin)
    if data is None:
        raise errors.RequestError("There was an error while fetching the coin data")

    price_change_perc_24h = data["price_change_percentage_24h"]
    price_change_perc_7d = data["price_change_percentage_7d"]
    price_change_perc_30d = data["price_change_percentage_30d"]

    # Add + in front of the positive percentages to show green color (- comes from api itself for negatives)
    if price_change_perc_24h >= 0:
        price_change_perc_24h = "+" + str(price_change_perc_24h)
    if price_change_perc_7d >= 0:
        price_change_perc_7d = "+" + str(price_change_perc_7d)
    if price_change_perc_30d >= 0:
        price_change_perc_30d = "+" + str(price_change_perc_30d)

    await pretty_print(
        ctx,
        pretty_embed(
            [
                {
                    "name": "Current Price",
                    "value": f"```diff\n${data['current_price']}```",
                    "inline": False,
                },
                {
                    "name": "24h Price Change",
                    "value": f"```diff\n{price_change_perc_24h}%\n```",
                },
                {
                    "name": "7d Price Change",
                    "value": f"```diff\n{price_change_perc_7d}%```",
                },
                {
                    "name": "30d Price Change",
                    "value": f"```diff\n{price_change_perc_30d}%```",
                },
                {
                    "name": "24h Low",
                    "value": f"```diff\n{data['low_24h']}```",
                },
                {
                    "name": "24h High",
                    "value": f"```diff\n{data['high_24h']}```",
                },
                {
                    "name": "Market Cap Rank",
                    "value": f"```diff\n{data['market_cap_rank']}```",
                },
            ],
            title=f"{coin} Price Statistics",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )


async def balance(
    self,
    ctx: SlashContext,
    address,
):
    balances = economy_api.get_balances(address)
    if balances is None:
        raise errors.RequestError("There was an error while fetching the balances")

    balance_fields = []
    for balance in balances:
        balance_fields.extend(
            [
                {
                    "name": "Denom",
                    "value": balance["denom"],
                },
                {
                    "name": "Amount",
                    "value": balance["amount"],
                },
                {
                    "name": "\u200b",
                    "value": "\u200b",
                },
            ]
        )

    await pretty_print(
        ctx,
        pretty_embed(
            balance_fields,
            title=f"Balances of {address}",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )


async def inflation(self, ctx: SlashContext):
    inflation = economy_api.get_inflation()
    if inflation is None:
        raise errors.RequestError("There was an error while fetching the inflation")

    await pretty_print(
        ctx,
        pretty_embed(
            [
                {
                    "name": "Current minting inflation value",
                    "value": inflation,
                },
            ],
            title="Inflation",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )


async def community_pool(self, ctx: SlashContext):
    pools = economy_api.get_community_pools()
    if pools is None:
        raise errors.RequestError(
            "There was an error while fetching the community pool"
        )

    pool_fields = []
    for pool in pools:
        pool_fields.extend(
            [
                {
                    "name": "Denom",
                    "value": pool["denom"],
                },
                {
                    "name": "Amount",
                    "value": pool["amount"],
                },
                {
                    "name": "\u200b",
                    "value": "\u200b",
                },
            ]
        )

    await pretty_print(
        ctx,
        pretty_embed(
            pool_fields,
            title="Community Pool",
            timestamp=True,
            color=WHITE_COLOR,
        ),
    )
