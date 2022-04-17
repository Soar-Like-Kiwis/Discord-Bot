import logging

import disnake
from disnake.ext import commands

from slk.cog_utils.favicon_leakage import check_site_leaks_framework
from slk.exceptions import UnknownFavicon, UnknownFramework

log = logging.getLogger(__name__)


class FaviconLeakageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f"{self.__class__.__name__}: Ready")

    @commands.slash_command()
    async def favicon(self, inter: disnake.AppCommandInteraction):
        pass

    @favicon.sub_command()
    async def checker(self, interation: disnake.AppCommandInteraction, url: str):
        """Try figure out a framework for the given favicon."""
        try:
            framework = await check_site_leaks_framework(url)
        except UnknownFavicon:
            await interation.send("This url did not resolve correct.", ephemeral=True)
        except UnknownFramework:
            await interation.send("Could not figure out a framework.", ephemeral=True)
        else:
            await interation.send(
                embed=disnake.Embed(
                    title="Found a match",
                    timestamp=interation.created_at,
                    description=f"**Framework:**\n`{framework}`\n\n**Url:**\n[{url}]({url})",
                ),
                ephemeral=True,
            )


def setup(bot):
    bot.add_cog(FaviconLeakageCog(bot))
