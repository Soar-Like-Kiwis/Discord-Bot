from typing import Dict

import disnake


class SkillResource:
    def __init__(
        self,
        skill: str,
        resource_link: str,
        resource_overview: str,
        _id=None,
    ):
        self.skill: str = skill
        self.resource_link: str = resource_link
        self.resource_overview: str = resource_overview
        self._id = _id

    def as_dict(self) -> Dict:
        data = {
            "skill": self.skill.lower(),
            "resource_link": self.resource_link,
            "resource_overview": self.resource_overview,
        }
        if self._id:
            data["_id"] = self._id

        return data

    def unique_filter(self) -> Dict:
        return {"resource_link": self.resource_link}

    def as_select_option(self) -> disnake.SelectOption:
        return disnake.SelectOption(
            label=self.resource_overview,
            description=self.resource_link,
            value=self.resource_link,
        )
