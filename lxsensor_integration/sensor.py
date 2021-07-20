import logging
from datetime import timedelta
from ast import literal_eval


from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.const import ATTR_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_DEVICES

from homeassistant.const import (
    LIGHT_LUX
)

from .const import DOMAIN,CONF_DEVICEID,LX_SENSOR

ATTRIBUTION = ("LUXSENSOR _ EKO ML-020SO")

DEFAULT_NAME = "EKO_ML_020SO"

_LOGGER = logging.getLogger(__name__)

#SCAN_INTERVAL = timedelta(seconds=30)

STATUS_CATEGORY = [
    "lux"
]

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][LX_SENSOR]
    #_LOGGER.info(f"navien coordinator : {coordinator}")

    entities = []
    for i,status_category in enumerate(STATUS_CATEGORY):
        entities.append(LuxBaseSensor(coordinator, config_entry.data, status_category))

    async_add_entities(entities)
    
    #entities.append(NavienBaseSensor(coordinator,config_entry.data))

class LuxBaseSensor(CoordinatorEntity,Entity):

    def __init__(self, coordinator, config, STATUS_CATEGORY):
        """Initialise the platform with a data instance and site."""
        super().__init__(coordinator)
        self._config = config
        self._data_type = STATUS_CATEGORY
        #self._current_operationmode = NavienAirone(deviceid=self._config.get(CONF_DEVICEID))

    @property
    def unique_id(self):
        """Return unique ID."""
        _LOGGER.info(f"navien def unique_id {self._config[CONF_DEVICEID]}{self._data_type}")
        return f"{self._config[CONF_DEVICEID]} {self._data_type}"

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self._config.get(CONF_DEVICEID)
        _LOGGER.info(f"navien def name {DEFAULT_NAME} {self._data_type}")
        return f"{DEFAULT_NAME} {self._data_type}"

    @property
    def state(self):
        if self.coordinator.data.current_status_data == None:
            return "uploading.."

        if self._data_type == "lux":
            _LOGGER.info(f"lxdebug self.coordinator.data.current_status_data: {self.coordinator.data.current_status_data}")
            temp1 = self.coordinator.data.current_status_data.decode()
            temp2 = temp1.split(',')
            _LOGGER.info(f"lxdebug temp2: {temp2}")
            temp3 = temp2[1].split(':')
            _LOGGER.info(f"lxdebug temp3: {temp3}")
            return temp3[1]

    @property
    def unit_of_measurement(self):
        if self._data_type == "lux":
            return LIGHT_LUX

    @property
    def attribution(sefl):
        return ATTRIBUTION

    @property
    def device_info(self):
        """Device info."""
        return {
            "identifiers": {(DOMAIN,)},
            "manufacturer": "EKO",
            "model": "ML_020SO",
            "default_name": "EKO_ML_020SO",
            "entry_type": "device", ##
        }