
"""
Support for the Netatmo devices.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/netatmo/
"""
import logging
from datetime import timedelta
from urllib.error import HTTPError
import voluptuous as vol
from homeassistant.const import (
    CONF_API_KEY, CONF_PASSWORD, CONF_USERNAME, CONF_DISCOVERY)
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

REQUIREMENTS = [
    'https://github.com/samueldumont/netatmo-api-python/archive/'
    'v0.9.2-vaillant.zip#lnetatmo==0.9.2-vaillant']

_LOGGER = logging.getLogger(__name__)

CONF_SECRET_KEY = 'secret_key'
CONF_USER_PREFIX = 'user_prefix'
CONF_APP_VERSION = 'app_version'

DOMAIN = 'vaillant'

NETATMO_AUTH = None
DEFAULT_DISCOVERY = True

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)
MIN_TIME_BETWEEN_EVENT_UPDATES = timedelta(seconds=10)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_SECRET_KEY): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Optional(CONF_DISCOVERY, default=DEFAULT_DISCOVERY): cv.boolean,
        vol.Optional(CONF_APP_VERSION, default="1.0.4.0"): cv.string,
        vol.Optional(CONF_USER_PREFIX, default="vaillant"): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the Netatmo devices."""
    import lnetatmo

    global NETATMO_AUTH
    try:
      NETATMO_AUTH = lnetatmo.ClientAuth(
            config[DOMAIN][CONF_API_KEY], config[DOMAIN][CONF_SECRET_KEY],
            config[DOMAIN][CONF_USERNAME], config[DOMAIN][CONF_PASSWORD],
            'read_station read_camera access_camera '
            'read_thermostat write_thermostat '
            'read_presence access_presence',
            config[DOMAIN][CONF_APP_VERSION], config[DOMAIN][CONF_USER_PREFIX])

    except HTTPError:
        _LOGGER.error("Unable to connect to Netatmo API")
        return False

    if config[DOMAIN][CONF_DISCOVERY]:
        discovery.load_platform(hass, 'climate', DOMAIN, {}, config)

    return True
