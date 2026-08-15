# The APIs

One subpackage per Open-Meteo service. Every subpackage follows the same
shape: a client preset to the service's base URL, one operation class
per endpoint (`GetV1Forecast`, `SearchLocations`, ...), enums for the
enumerable request parameters, and dataclass models for the responses.
Import everything from the subpackage root — e.g.
`from action0.open_meteo.marine import MarineClient`.

| Subpackage | Client | Default base URL |
|---|---|---|
| `forecast` | `ForecastClient` | `https://api.open-meteo.com` |
| `historical_weather` | `HistoricalWeatherClient` | `https://archive-api.open-meteo.com` |
| `air_quality` | `AirQualityClient` | `https://air-quality-api.open-meteo.com` |
| `marine` | `MarineClient` | `https://marine-api.open-meteo.com` |
| `ensemble` | `EnsembleClient` | `https://ensemble-api.open-meteo.com` |
| `seasonal` | `SeasonalClient` | `https://seasonal-api.open-meteo.com` |
| `climate` | `ClimateClient` | `https://climate-api.open-meteo.com` |
| `flood` | `FloodClient` | `https://flood-api.open-meteo.com` |
| `elevation` | `ElevationClient` | `https://api.open-meteo.com` |
| `geocoding` | `GeocodingClient` | `https://geocoding-api.open-meteo.com` |

## Weather forecast — `forecast`

[Docs](https://open-meteo.com/en/docs) ·
`GetV1Forecast` returns hourly, daily, 15-minutely and current weather
for up to 16 forecast days:

```python
from action0.open_meteo.forecast import ForecastClient, GetV1Forecast, GetV1ForecastDailyItem

client = ForecastClient(backend)
weather = client.send(
    GetV1Forecast(
        latitude="48.21",
        longitude="16.37",
        daily=[GetV1ForecastDailyItem.TEMPERATURE_2M_MAX, GetV1ForecastDailyItem.SUNRISE],
        timezone="Europe/Vienna",
    )
)
```

## Historical weather — `historical_weather`

[Docs](https://open-meteo.com/en/docs/historical-weather-api) ·
`GetV1Archive` serves reanalysis data from 1940 onwards; `start_date=`
and `end_date=` are `datetime.date`:

```python
import datetime

from action0.open_meteo.historical_weather import (
    GetV1Archive,
    GetV1ArchiveHourlyItem,
    HistoricalWeatherClient,
)

client = HistoricalWeatherClient(backend)
past = client.send(
    GetV1Archive(
        latitude="48.21",
        longitude="16.37",
        start_date=datetime.date(1990, 1, 1),
        end_date=datetime.date(1990, 12, 31),
        hourly=[GetV1ArchiveHourlyItem.TEMPERATURE_2M],
    )
)
```

## Air quality — `air_quality`

[Docs](https://open-meteo.com/en/docs/air-quality-api) ·
`GetV1AirQuality`: pollutants, pollen and AQI indices:

```python
from action0.open_meteo.air_quality import (
    AirQualityClient,
    GetV1AirQuality,
    GetV1AirQualityHourlyItem,
)

client = AirQualityClient(backend)
air = client.send(
    GetV1AirQuality(
        latitude="48.21",
        longitude="16.37",
        hourly=[GetV1AirQualityHourlyItem.PM10, GetV1AirQualityHourlyItem.EUROPEAN_AQI],
    )
)
```

## Marine weather — `marine`

[Docs](https://open-meteo.com/en/docs/marine-weather-api) ·
`GetV1Marine`: wave height, direction, period and swell.

## Ensemble forecasts — `ensemble`

[Docs](https://open-meteo.com/en/docs/ensemble-api) ·
`GetV1Ensemble` returns *every member* of an ensemble model run. The
members arrive as dynamic JSON keys (`temperature_2m_member01`, ...), so
they land in the models' typed catch-all field:

```python
from action0.open_meteo.ensemble import EnsembleClient, GetV1Ensemble, GetV1EnsembleHourlyItem

client = EnsembleClient(backend)
runs = client.send(
    GetV1Ensemble(
        latitude="48.21",
        longitude="16.37",
        hourly=[GetV1EnsembleHourlyItem.TEMPERATURE_2M],
    )
)
assert runs.hourly is not None and runs.hourly.additional_properties is not None
member01 = runs.hourly.additional_properties["temperature_2m_member01"]  # list[float]
```

## Seasonal forecasts — `seasonal`

[Docs](https://open-meteo.com/en/docs/seasonal-forecast-api) ·
`GetV1Seasonal`: up to nine months ahead; like the ensemble API, the
per-member values arrive in the catch-all field.

## Climate change projections — `climate`

[Docs](https://open-meteo.com/en/docs/climate-api) ·
`GetV1Climate`: CMIP6 downscaled projections from 1950 to 2050; pick the
climate models via the `models=` enum list.

## Flood — `flood`

[Docs](https://open-meteo.com/en/docs/flood-api) ·
`GetV1Flood`: GloFAS river discharge, daily, up to 30 years back.

## Elevation — `elevation`

[Docs](https://open-meteo.com/en/docs/elevation-api) ·
`GetV1Elevation` resolves coordinates to terrain elevation (90 m DEM);
it shares `api.open-meteo.com` with the forecast service.

## Geocoding — `geocoding`

[Docs](https://open-meteo.com/en/docs/geocoding-api) ·
`SearchLocations` turns place names (or postal codes) into coordinates,
`GetLocation` looks a single location up by its GeoNames id — see the
{doc}`quickstart` for the name-to-forecast flow. This is the one service
whose schema is written by this project (upstream publishes none, see
{doc}`generation`).
