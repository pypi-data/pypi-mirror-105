from .session import Session


class Humidifier:
    """Class that represents a humidifier object in the Venta API."""

    def __init__(self, raw_data: dict, session: Session):
        """Initialize a humidifier object."""
        self.raw_data = raw_data
        self.session = session

    # Note: each property name maps the name in the returned data

    @property
    def mac(self) -> int:
        """Return the Mac of the humidifier."""
        return self.raw_data["Header"]["MacAdress"]

    @property
    def temperature(self) -> int:
        """Return the name of the humidifier."""
        return self.raw_data["Measure"]["Temperature"]

    @property
    def humidity(self) -> int:
        """Return the name of the humidifier."""
        return self.raw_data["Measure"]["Humidity"]

    @property
    def dust(self) -> int:
        """Return the name of the humidifier."""
        return self.raw_data["Measure"]["Dust"]

    @property
    def target_humidity(self) -> int:
        """Return the name of the humidifier."""
        return self.raw_data["Action"]["TargetHum"]

    @property
    def fan_speed(self) -> int:
        """Return the name of the humidifier."""
        return self.raw_data["Action"]["FanSpeed"]

    @property
    def is_on(self) -> bool:
        """Return the name of the humidifier."""
        return self.raw_data["Action"]["Power"]

    @property
    def is_sleep_mode(self) -> bool:
        """Return if the humidifier is on."""
        return self.raw_data["Action"]["SleepMode"]

    @property
    def is_auto_mode(self) -> bool:
        """Return if the humidifier is on."""
        return self.raw_data["Action"]["Automatic"]

    async def set_humidity(self, humidity: int):
        res = await self.session.request(json={"Action":
                                               {"TargetHum": humidity}
                                               })
        res.raise_for_status()
        self.raw_data = await res.json(content_type='text/plain')

    async def change_mode(self, mode: str, speed: int = 0):
        turn_off = {"Action":
                    {"Power": False}
                    }

        turn_on = {"Action":
                   {"Power": True}
                   }

        sleep_mode = {"Action":
                      {"Power": True,
                       "SleepMode": True,
                       "Automatic": False}
                      }

        automatic_mode = {"Action":
                          {"Power": True,
                           "SleepMode": False,
                           "Automatic": True}
                          }

        def fan_speed_mode(self, speed):
            return {"Action":
                    {"Power": True,
                     "SleepMode": False,
                     "Automatic": False,
                     "FanSpeed": speed}
                    }

        if (mode == 'off'):
            action = turn_off
        elif (mode == 'on'):
            action = turn_on
        elif (mode == 'sleep'):
            action = sleep_mode
        elif (mode == 'automatic'):
            action = automatic_mode
        elif (mode == 'manual'):
            action = fan_speed_mode(speed)

        res = await self.session.request(json=action)
        res.raise_for_status()
        self.raw_data = await res.json(content_type='text/plain')

    async def async_update(self):
        """Update the humidifier data."""
        res = await self.session.request()
        res.raise_for_status()
        self.raw_data = await res.json(content_type='text/plain')
