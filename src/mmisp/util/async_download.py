import asyncio
from typing import Optional, Self

from aiohttp import ClientSession
from yarl import URL


class Response:
    """Represents the response from an HTTP request.

    Attributes:
        status: The HTTP status code of the response.
        reason: The reason phrase associated with the status code.
        data: The response body as a string.
        url: The URL of the request.
        ok: A boolean indicating whether the request was successful (status code 2xx).
    """

    def __init__(self: Self, status: int, reason: Optional[str], data: str, url: URL, ok: bool) -> None:
        """Initializes a Response object.

        Args:
            status: The HTTP status code.
            reason: The reason phrase for the status code.
            data: The response body.
            url: The URL of the request.
            ok: Whether the request was successful.
        """
        self.status = status
        self.reason = reason
        self.data = data
        self.url = url
        self.ok = ok


async def download_files(session: ClientSession, urls: list[str]) -> list[Response]:
    """Downloads multiple files asynchronously.

    Args:
        session: The aiohttp client session.
        urls: A list of URLs to download.

    Returns:
        list[Response]: A list of Response objects for each URL.
    """
    tasks = []
    for url in urls:
        task = asyncio.create_task(download_file(session, url))
        tasks.append(task)

    return await asyncio.gather(*tasks)


async def download_file(session: ClientSession, url: str) -> Response:
    """Downloads a single file asynchronously.

    Args:
        session: The aiohttp client session.
        url: The URL to download.

    Returns:
        Response: The response object containing the result of the request.
    """
    async with session.get(url) as response:
        result = Response(response.status, response.reason, await response.text(), response.url, response.ok)
        return result
