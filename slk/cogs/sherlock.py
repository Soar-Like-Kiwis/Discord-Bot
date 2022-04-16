import logging
import os
from typing import TYPE_CHECKING

import disnake
from bot_base.paginators.disnake_paginator import DisnakePaginator
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

        paginator: DisnakePaginator = DisnakePaginator(
            15,
            result,
            page_formatter=lambda paginator, page_items, page_number: disnake.Embed(
                description="\n".join(item for item in page_items)
            ).set_footer(text=f"Page {page_number}/{paginator.total_pages}"),
        )
        await paginator.start(inter)
        log.info(
            "%s requested sherlock for the username %s",
            inter.user.display_name,
            username,
        )


def setup(bot):
    bot.add_cog(SherlockCog(bot))
