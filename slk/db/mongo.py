from bot_base.db import MongoManager


class SLKMongoManager(MongoManager):
    def __init__(self, connection_url):
        super().__init__(connection_url=connection_url, database_name="soar_like_kiwis")
