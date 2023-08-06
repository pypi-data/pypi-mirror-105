from .session import Session


class Light:
    """Class that represents a light object in the Venta API."""

    def __init__(self, raw_data: dict, session: Session):
        """Initialize a light object."""
        self.raw_data = raw_data
        self.session = session

    @property
    def is_light_on(self) -> bool:
        """Return if the light is on."""
        return self.raw_data["Action"]["LEDStripActive"]

    @property
    def light_color(self) -> str:
        """Return color of the light."""
        return self.raw_data["Action"]["LEDStrip"]

    async def control(self, status: bool = True, color: str = "#0000ff"):
        """Control the light."""
        res = await self.session.request(json={"Action":
                                               {"LEDStripActive": status,
                                                "LEDStrip": color}
                                               })
        res.raise_for_status()
        self.raw_data = await res.json(content_type='text/plain')

    async def update(self):
        """Fetch the light data."""
        res = await self.session.request()
        res.raise_for_status()
        self.raw_data = await res.json(content_type='text/plain')
