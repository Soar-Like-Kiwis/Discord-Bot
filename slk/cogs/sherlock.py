import logging
import os
from io import BytesIO
from typing import TYPE_CHECKING

import disnake
from disnake.ext import commands

from slk.cog_utils.sherlock import Sherlock

if TYPE_CHECKING:
    from slk import SLK

log = logging.getLogger(__name__)


class SherlockCog(commands.Cog):
    """Provides sherlock functionality."""

    def __init__(self, bot: "SLK"):
        self.bot: "SLK" = bot
        self.sherlock: Sherlock = Sherlock(
            os.path.join(os.getcwd(), "slk", "cog_utils")
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f"{self.__class__.__name__}: Ready")

    @commands.slash_command()
    async def sherlock(
        self, inter: disnake.ApplicationCommandInteraction, username: str
    ):
        """Lookup a username using Sherlock."""
        await inter.send("Working on it!", ephemeral=True)
        result = await self.sherlock.request(username)
        sorted_results = "\n".join([r for r in result])
        buffer = BytesIO(sorted_results.encode("utf-8"))
        msg = await inter.original_message()
        await msg.edit(
            "Check the file!",
            file=disnake.File(buffer, filename="results.md"),
        )
        log.info(
            "%s requested sherlock for the username %s",
            inter.user.display_name,
            username,
        )


def setup(bot):
    bot.add_cog(SherlockCog(bot))
