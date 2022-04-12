import os
from typing import Set

from bot_base import BotBase

from slk.db import SLKMongoManager


class SLK(BotBase):
    def __init__(self, *args, **kwargs):
        self.db: SLKMongoManager = SLKMongoManager(os.environ["MONGO_URL"])
        super().__init__(*args, **kwargs, leave_db=True)

        self.team_members: Set = {
            271612318947868673,  # Skelmis
            218213931968102400,  # Riddle
            155576095750488064,  # Darts
            898718974316015657,  # cece
            342100056658149387,  # LINNY
        }
