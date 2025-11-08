"""Integration 101 Template integration using DataUpdateCoordinator."""

from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import DOMAIN, HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL
from .heat_pump import HeatPump, Sensor, SensorData, SENSORS

_LOGGER = logging.getLogger(__name__)


@dataclass
class ExampleAPIData:
    """Class to hold api data."""
    sensor_data: list[SensorData]
    sensor_config: list[Sensor]


class ExampleCoordinator(DataUpdateCoordinator):
    """My example coordinator."""

    data: ExampleAPIData

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize coordinator."""

        # Set variables from values entered in config flow setup
        self.host = config_entry.data[CONF_HOST]

        # set variables from options.  You need a default here incase options have not been set
        self.poll_interval = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        # Initialise DataUpdateCoordinator
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            # Method to call on every update interval.
            update_method=self.async_update_data,
            # Polling interval. Will only be polled if there are subscribers.
            # Using config option here but you can just use a value.
            update_interval=timedelta(seconds=self.poll_interval),
        )

        self.port: int = 3000  # Default port for the heat pump
        
        # Initialise your api here
        self.heat_pump = HeatPump(self.host, self.port)

    async def async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        sensor_list = SENSORS
        sensor_data = self.heat_pump.sensor_data

        # What is returned here is stored in self.data by the DataUpdateCoordinator
        return ExampleAPIData(
            sensor_data=sensor_data,
            sensor_config=sensor_list,
        )