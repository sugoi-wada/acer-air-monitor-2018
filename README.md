# Acer Air Monitor for Home Assistant

Home Assistant integration for Acer Air Monitor.

This integration allows you to add Air Monitor sensors to your home assistant.

NOTE: The product page seems to be closed now, but you can view it [here](https://web.archive.org/web/20181018025644/http://home.cloud.acer.com/tw/airmonitor/) (web archive).

**This component will set up the following sensors.**

- `CO2`
- `PM2.5`
- `PM10`
- `Illuminance`
- `Humidity`
- `Temperature`
- `TVOC`
- `IAQ`

## Requirement

Connect your Acer account and device with the Acer Air Monitor 2018 app ([Android](https://play.google.com/store/apps/details?id=com.acer.airmonitor2) / [iOS](https://apps.apple.com/tw/app/acer-air-monitor-2018/id1378898931)).

## Installation

### Via HACS

Search and install `Acer Air Monitor` in HACS

### Manually

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `acer_air_monitor`.
4. Download _all_ the files from the `custom_components/acer_air_monitor/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Acer Air Monitor"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/acer_air_monitor/translations/en.json
custom_components/acer_air_monitor/translations/nb.json
custom_components/acer_air_monitor/translations/sensor.nb.json
custom_components/acer_air_monitor/__init__.py
custom_components/acer_air_monitor/api.py
custom_components/acer_air_monitor/binary_sensor.py
custom_components/acer_air_monitor/config_flow.py
custom_components/acer_air_monitor/const.py
custom_components/acer_air_monitor/manifest.json
custom_components/acer_air_monitor/sensor.py
custom_components/acer_air_monitor/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
