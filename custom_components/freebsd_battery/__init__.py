"""Details about the built-in battery."""
import logging
import os

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import ATTR_NAME, CONF_NAME, DEVICE_CLASS_BATTERY, PERCENTAGE
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ATTR_CAPACITY_LEVEL = "capacity_level"
ATTR_STATUS = "status"

BATTERY_LIFE_COMMAND = "sysctl hw.acpi.battery.life  | cut -d' ' -f2"
BATTERY_STATUS_COMMAND = "sysctl hw.acpi.battery.state | cut -d' ' -f2"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Linux Battery sensor."""
    name = config.get(CONF_NAME)
    add_entities([LinuxBatterySensor(name)], True)


class LinuxBatterySensor(SensorEntity):
    """Representation of a Linux Battery sensor."""

    def __init__(self, name):
        """Initialize the battery sensor."""
        self._name = name
        self._battery_stat = {
            ATTR_CAPACITY_LEVEL: None,
            ATTR_STATUS: None
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return DEVICE_CLASS_BATTERY

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._battery_stat

    @property
    def native_unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return PERCENTAGE

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {
            ATTR_CAPACITY_LEVEL: self._battery_stat[ATTR_CAPACITY_LEVEL],
            ATTR_STATUS: self._battery_stat[ATTR_STATUS],
        }

    def update(self):
        """Get the latest data and updates the states."""
        battery_life = int(os.system(BATTERY_LIFE_COMMAND))
        battery_status = os.system(BATTERY_STATUS_COMMAND) == "1"
        self._battery_stat[ATTR_CAPACITY_LEVEL] = battery_life
        self._battery_stat[ATTR_STATUS] = battery_status
