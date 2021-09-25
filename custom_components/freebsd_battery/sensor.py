"""Details about the built-in battery."""
from __future__ import annotations
import logging
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
import os

from homeassistant.const import DEVICE_CLASS_BATTERY, PERCENTAGE
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ATTR_CAPACITY_LEVEL = "capacity_level"
ATTR_STATUS = "status"

BATTERY_LIFE_COMMAND = "sysctl hw.acpi.battery.life  | cut -d' ' -f2"
BATTERY_STATUS_COMMAND = "sysctl hw.acpi.battery.state | cut -d' ' -f2"

"""Platform for sensor integration."""


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([FreeBSDBattery()])


class FreeBSDBattery(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._battery_life = None
        self._battery_status = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'FreeBSD Battery'

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._battery_life

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def device_class(self):
        return DEVICE_CLASS_BATTERY

    @property
    def extra_state_attributes(self):
        return {
            "life": self._battery_life,
            "status": self._battery_status
        }

    def update(self):
        """Get the latest data and updates the states."""
        self._battery_life = int(os.system(BATTERY_LIFE_COMMAND))
        self._battery_status = int(os.system(BATTERY_STATUS_COMMAND))
        _LOGGER.log(1, self._battery_life)
        _LOGGER.log(1, self._battery_status)
