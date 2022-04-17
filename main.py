import logging
import os

import disnake
from disnake.ext import commands

from slk import SLK

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    datefmt="%I:%M:%S %p %d/%m/%Y",
    format="%(levelname)-7s | %(asctime)s | %(filename)15s:%(funcName)-25s | %(message)s",
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
    test_guilds=[963306196792639529],
    description="Powering Soar Like Kiwi's",
)


@bot.listen("on_ready")
async def on_ready():
    log.info("Main: Ready")


@bot.listen("on_member_join")
async def on_member_join(member: disnake.Member):
    if member.id in bot.team_members:
        role = member.guild.get_role(963306655657898004)
        await member.add_roles(role, reason="Team member.")
        log.info(
            "Gave Role(id=963306655657898004, name=%s) to %s as they are registered members.",
            role.name,
            member.display_name,
        )


@bot.event
async def on_slash_command_error(inter: disnake.Interaction, error):
    if isinstance(error, commands.errors.MissingRole):
        assert isinstance(inter, disnake.ApplicationCommandInteraction)
        role = inter.guild.get_role(error.missing_role)
        await inter.send(
            f"You need the `{role.name}` role to run this command :shrug:",
            ephemeral=True,
        )
        log.error(
            "%s tried to run '%s', however the lacked the Role(id=%s, name='%s')",
            inter.user.display_name,
            inter.application_command.qualified_name,
            role.id,
            role.name,
        )

    else:
        await inter.send("Looks like something went wrong :shrug:", ephemeral=True)
        raise error


if __name__ == "__main__":
    bot.load_extension("slk.cogs.resources")
    bot.load_extension("slk.cogs.sherlock")
    bot.load_extension("slk.cogs.favicon_leakage")
    bot.run(os.environ["TOKEN"])
