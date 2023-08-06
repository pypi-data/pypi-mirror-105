from aiohttp import ClientSession, ClientResponse
import asyncio


class Session:
    def __init__(self, websession: ClientSession, host: str):
        self.websession = websession
        self.host = host

    async def request(self, **kwargs) -> ClientResponse:
        return await self.websession.request(
            "POST", f"{self.host}/datastructure", **kwargs,
        )
