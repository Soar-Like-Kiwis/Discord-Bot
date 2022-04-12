import logging
import os

import disnake

from slk import SLK

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    datefmt="%I:%M:%S %p %d/%m/%Y",
    format="%(levelname)-7s | %(asctime)s | %(filename)12s:%(funcName)-12s | %(message)s",
)
gateway_logger = logging.getLogger("disnake.gateway")
gateway_logger.setLevel(logging.WARNING)
client_logger = logging.getLogger("disnake.client")
client_logger.setLevel(logging.WARNING)
http_logger = logging.getLogger("disnake.http")
http_logger.setLevel(logging.WARNING)

bot = SLK(
    command_prefix="slk.",
    case_insensitive=True,
    strip_after_prefix=True,
    load_builtin_commands=True,
    intents=disnake.Intents.all(),
    description="Powering Soar Like Kiwi's",
)


@bot.listen("on_ready")
async def on_ready():
    log.info("Ready")


@bot.listen("on_member_join")
async def on_member_join(member: disnake.Member):
    if member.id in bot.team_members:
        role = member.guild.get_role(963306655657898004)
        await member.add_roles(role, reason="Team member.")


if __name__ == "__main__":
    bot.run(os.environ["TOKEN"])
