from .session import Session
from .light import Light
from .humidifier import Humidifier


class VentaAPI:
    def __init__(self, session: Session):
        self.session = session

    async def get_light(self) -> Light:
        """Get light instance"""
        res = await self.session.request()
        res.raise_for_status()
        return Light(await res.json(content_type='text/plain'), self.session)

    async def get_humidifier(self) -> Humidifier:
        """Get humidifier instance"""
        res = await self.session.request()
        res.raise_for_status()
        return Humidifier(await res.json(content_type='text/plain'),
                          self.session)
