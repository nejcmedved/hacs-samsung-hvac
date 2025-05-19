import threading
import time
import logging
from enum import StrEnum
from typing import List
from dataclasses import dataclass
from typing import Any
_LOGGER = logging.getLogger(__name__)

class SensorType(StrEnum):
    """Device types."""

    TEMP_SENSOR = "temp_sensor"
    OTHER = "other"
    BINARY_SENSOR = "binary_sensor"


@dataclass
class Sensor:
    """Class to hold sensor data."""
    id: str
    type: SensorType
    name: str

    def __str__(self) -> str:
        """Return string representation of the sensor."""
        return f"{self.name} ({self.type})"


SENSORS: List[Sensor] = [
    Sensor(id="outdoor_temp", type=SensorType.TEMP_SENSOR, name="Outdoor temperature"),
    Sensor(id="comm_state", type=SensorType.BINARY_SENSOR, name="Communication state"),
]

@dataclass
class SensorData:
    """Class to hold sensor data."""
    id: int
    value: Any

    def __str__(self) -> str:
        """Return string representation of the sensor data."""
        return f"Sensor {self.id}: {self.value}"

class HeatPump(threading.Thread):
    def __init__(self, ip: str, port:int):
        super().__init__()
        self.ip = ip
        self.port = port
        self._is_running = False
        self.daemon = True
        self.sensor_data: List[SensorData] = []
        self.start()    
            
    def run(self):
        self._is_running = True
        # Simulate some work being done in the thread
        while self._is_running:
            _LOGGER.info(f"HeatPump running on {self.ip}:{self.port}")
            time.sleep(1)