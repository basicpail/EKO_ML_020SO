"""Config flow for navien_airone."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol


from homeassistant import config_entries
from homeassistant.helpers.typing import ConfigType
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN,CONF_DEVICEID

_LOGGER = logging.getLogger(__name__)


class LuxSensorFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a navien config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize"""
        self._errors = {}
        self.deviceid = None

    async def async_step_user(
        self, user_input: Optional[ConfigType] = None
    ) -> Dict[str, Any]:
        """Handle a flow initiated by the user."""
        try:
            if user_input:
                _LOGGER.info(f"navien DOMAIN:{DOMAIN}, user_input: {user_input}")
                return self.async_create_entry(
                    title=f"{DOMAIN}_" + user_input[CONF_DEVICEID], data=user_input
                )      
        except:
            return await self._show_config_form()


        return await self._show_config_form()


    async def _show_config_form(
        self,
    ):
        """Show the configuration form to edit device data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICEID): str,
                }
            ),
            errors=self._errors,
        )
