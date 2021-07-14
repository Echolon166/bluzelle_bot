from discord import Color

"""
    Constants useful for data module
"""

CHANNEL_PREFIXES_TABLE = "channel_prefixes"
COMMANDS_TABLE = "commands"

GUILD_ID_KEY = "guildId"
PREFIX_KEY = "prefix"

NAME_KEY = "name"
DESCRIPTION_KEY = "description"

"""
    URL constants
"""
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
BLUZELLE_PRIVATE_TESTNET_URL = "https://client.sentry.testnet.private.bluzelle.com"

BLUZELLE_RPC_PORT = "26657"
BLUZELLE_API_PORT = "1317"

"""
    Miscellaneous constants
"""

ERROR_COLOR = Color(0xFF0000)
SUCCESS_COLOR = Color(0x0000FF)
WHITE_COLOR = Color(0xFFFFFE)
