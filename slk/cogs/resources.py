import logging
from typing import TYPE_CHECKING, List, Optional

import disnake
from bot_base.db import Document
from disnake import TextInputStyle, SelectOption
from disnake.ext import commands
from pymongo.results import DeleteResult

from slk.db import SkillResource

if TYPE_CHECKING:
    from slk import SLK

log = logging.getLogger(__name__)


class ResourceCog(commands.Cog):
    """Provides various resources for each skill."""

    def __init__(self, bot: "SLK"):
        self.bot: "SLK" = bot
        self.skill_resources: Document = self.bot.db.skill_resources
        self.possible_skills = [
            "Pwn",
            "Boot2Root",
            "Forensics",
            "Cryptography",
            "Steganography",
            "Web Exploitation",
            "Binary Exploitation",
            "Reverse Engineering",
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f"{self.__class__.__name__}: Ready")

    @commands.slash_command()
    async def resources(
        self,
        inter: disnake.ApplicationCommandInteraction,
        skill: str,
    ):
        """Show resources for a given skill."""
        skill_resources: List[
            SkillResource
        ] = await self.skill_resources.find_many_by_custom({"skill": skill.lower()})

        embed = disnake.Embed(title=f"Resources for __{skill}__", description="")
        for sk in skill_resources:
            embed.description += (
                f"{sk.resource_overview}\nFind it [here]({sk.resource_link})\n\n"
            )

        if not skill_resources:
            embed.description = (
                "Doesn't look like I have specifics on this, "
                "have you tried googling it?"
            )

        await inter.send(embed=embed, ephemeral=True)
        log.info("Listed all resources for %s", inter.user.display_name)

    @resources.autocomplete("skill")
    async def skill_autocomplete(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user_input: str,
    ):
        return [
            skill
            for skill in self.possible_skills
            if user_input.lower() in skill.lower()
        ]

    @commands.slash_command()
    async def add(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @add.sub_command(name="resource")
    @commands.has_role(963306655657898004)
    async def add_resource(
        self,
        inter: disnake.ApplicationCommandInteraction,
        skill: str = commands.Param(
            choices=[
                "Pwn",
                "Boot2Root",
                "Forensics",
                "Cryptography",
                "Steganography",
                "Web Exploitation",
                "Binary Exploitation",
                "Reverse Engineering",
            ]
        ),
    ):
        """Add a new resource to the listed resources."""
        description = disnake.ui.TextInput(
            label="A short description of the resource",
            custom_id="description",
            max_length=100,
            style=TextInputStyle.paragraph,
        )
        link: disnake.ui.TextInput = disnake.ui.TextInput(
            label="Resource link",
            placeholder="https://your.link.here",
            custom_id="resource_link",
            max_length=100,
        )

        await inter.response.send_modal(
            custom_id="add_skill_resource",
            title="Add a new resource.",
            components=[
                description,
                link,
            ],
        )

        modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
            "modal_submit",
            check=lambda i: i.custom_id == "add_skill_resource"
            and i.author.id == inter.author.id,
            timeout=300,
        )

        sk: SkillResource = SkillResource(
            skill=skill,
            resource_link=modal_inter.text_values[link.custom_id],
            resource_overview=modal_inter.text_values[description.custom_id],
        )
        await self.skill_resources.upsert_custom(sk.unique_filter(), sk.as_dict())

        await modal_inter.send(
            f"Thanks! I have added that as a resource under __{skill}__.",
            ephemeral=True,
        )
        log.info(
            "New resource added by %s, category %s", inter.user.display_name, skill
        )

    @commands.slash_command()
    async def delete(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @delete.sub_command(name="resource")
    @commands.has_role(963306655657898004)
    async def delete_resource(
        self,
        inter: disnake.ApplicationCommandInteraction,
        skill: str = commands.Param(
            choices=[
                "Pwn",
                "Boot2Root",
                "Forensics",
                "Cryptography",
                "Steganography",
                "Web Exploitation",
                "Binary Exploitation",
                "Reverse Engineering",
            ]
        ),
    ):
        """Delete a resource from the listed resources."""
        current_skill_choices: List[
            SkillResource
        ] = await self.skill_resources.find_many_by_custom({"skill": skill.lower()})
        if not current_skill_choices:
            return await inter.send(
                "Doesn't look like any choices exist!", ephemeral=True
            )

        await inter.send(
            "Please pick the resource entry to delete.",
            components=disnake.ui.Select(
                custom_id="delete_resource",
                placeholder="The item to delete",
                max_values=len(current_skill_choices),
                options=[sk.as_select_option() for sk in current_skill_choices],
            ),
            ephemeral=True,
        )

        dropdown_inter: disnake.MessageInteraction = await self.bot.wait_for(
            "dropdown",
            check=lambda i: i.component.custom_id == "delete_resource"
            and i.author.id == inter.author.id,
            timeout=300,
        )
        await dropdown_inter.response.defer()

        deletion_count: int = 0
        for link in dropdown_inter.values:
            result: Optional[
                DeleteResult
            ] = await self.skill_resources.delete_by_custom(
                {"resource_link": link, "skill": skill.lower()}
            )
            if result:
                deletion_count += result.deleted_count

        sent_message: disnake.InteractionMessage = await inter.original_message()
        await sent_message.edit(
            f"I have deleted `{deletion_count}` resources for you.", components=None
        )
        log.info(
            "Deleted %s resources by command of %s",
            deletion_count,
            inter.user.display_name,
        )


def setup(bot):
    bot.add_cog(ResourceCog(bot))
