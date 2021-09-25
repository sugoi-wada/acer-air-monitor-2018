"""BlueprintEntity class"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.acer_air_monitor import BlueprintDataUpdateCoordinator

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION


class IntegrationBlueprintEntity(CoordinatorEntity):
    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, config_entry: ConfigEntry
    ):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
        }
