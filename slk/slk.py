import os

from bot_base import BotBase

from slk.db import SLKMongoManager


class SLK(BotBase):
    def __init__(self, *args, **kwargs):
        self.db: SLKMongoManager = SLKMongoManager(os.environ["MONGO_URL"])
        super().__init__(*args, **kwargs, leave_db=True)
