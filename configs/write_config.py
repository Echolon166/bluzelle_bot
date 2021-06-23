# python 3.x
from configparser import ConfigParser

config = ConfigParser(allow_no_value=True)
config.optionxform = str

config.add_section("DISCORD_BOT")
config.set(
    "DISCORD_BOT",
    "# Enter your API Secret Token here to connect to your discord bot.",
)
config.set(
    "DISCORD_BOT",
    "secret_token xxx",
)

with open("configs/config.ini", "w+") as f:
    config.write(f)
