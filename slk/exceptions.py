from disnake import DiscordException

class UnknownFavicon(DiscordException):
    """Unable to find a framework for this site."""


class UnknownFramework(DiscordException):
    """Unable to find a framework for this site."""