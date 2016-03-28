"""Helpers for config validation using voluptuous."""
import voluptuous as vol

from homeassistant.const import (
    CONF_PLATFORM, TEMP_CELCIUS, TEMP_FAHRENHEIT)
from homeassistant.helpers.entity import valid_entity_id
import homeassistant.util.dt as dt_util

# pylint: disable=invalid-name

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_PLATFORM): str,
}, extra=vol.ALLOW_EXTRA)

icon = vol.All(vol.Coerce(str), vol.truth(lambda val: val.startswith('mdi:')))
latitude = vol.All(vol.Coerce(float), vol.Range(min=-90, max=90))
longitude = vol.All(vol.Coerce(float), vol.Range(min=-180, max=180))


def entity_id(value):
    """Validate Entity ID."""
    if valid_entity_id(value):
        return value
    raise vol.Invalid('Entity ID {} does not match format <domain>.<object_id>'
                      .format(value))


def entity_ids(value):
    """Validate Entity IDs."""
    if isinstance(value, str):
        value = [ent_id.strip() for ent_id in value.split(',')]

    for ent_id in value:
        if not valid_entity_id(ent_id):
            raise vol.Invalid(
                'Entity ID {} does not match format <domain>.<object_id>'
                .format(ent_id))

    return value


def temperature_unit(value):
    """Validate and transform temperature unit."""
    if isinstance(value, str):
        value = value.upper()
        if value == 'C':
            return TEMP_CELCIUS
        elif value == 'F':
            return TEMP_FAHRENHEIT
    raise vol.Invalid('Invalid temperature unit. Expected: C or F')


def time_zone(value):
    """Validate timezone."""
    if dt_util.get_time_zone(value) is not None:
        return value
    raise vol.Invalid(
        'Invalid time zone passed in. Valid options can be found here: '
        'http://en.wikipedia.org/wiki/List_of_tz_database_time_zones')
