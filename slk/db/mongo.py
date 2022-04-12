from bot_base.db import MongoManager, Document

from slk.db import SkillResource


class SLKMongoManager(MongoManager):
    def __init__(self, connection_url):
        super().__init__(
            connection_url=connection_url,
            database_name="soar_like_kiwis",
        )

        self.skill_resources: Document = Document(
            self.db,
            "skill_resources",
            converter=SkillResource,
        )
