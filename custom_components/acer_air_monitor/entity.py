"""AirMonitorEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import AirMonitorDataUpdateCoordinator


class AirMonitorEntity(CoordinatorEntity):
    """AirMonitorEntity class."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: AirMonitorDataUpdateCoordinator) -> None:
        """Initialize."""
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.data["aopDeviceId"])},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )
        super().__init__(coordinator)
