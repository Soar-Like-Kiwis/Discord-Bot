import hashlib
from io import BytesIO

from PIL import Image, UnidentifiedImageError
import httpx

from .md5sums import FAVICON_SUMS
from slk.exceptions import UnknownFavicon, UnknownFramework


async def check_site_leaks_framework(url: str):
    """
    Given a url, attempt to extract the underlying
    framework from the favicon

    Raises
    ------
    UnknownFavicon
        ...
    UnknownFramework
        ...
    """
    try:
        async with httpx.AsyncClient() as client:
            favicon_request = await client.get(url)
    except Exception as e:
        raise UnknownFavicon from e

    md5hash = hashlib.md5(favicon_request.content)

    try:
        return FAVICON_SUMS[md5hash.hexdigest()]
    except KeyError:
        raise UnknownFramework from None
