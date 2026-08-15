# The APIs

One subpackage per Open-Meteo service, each with a page of its own.
Every subpackage follows the same shape: a client preset to the
service's base URL, one operation class per endpoint (`GetV1Forecast`,
`SearchLocations`, ...), enums for the enumerable request parameters,
and dataclass models for the responses. Import everything from the
subpackage root — e.g. `from action0.open_meteo.marine import
MarineClient`.

| Subpackage | Client | Default base URL |
|---|---|---|
| {doc}`forecast` | `ForecastClient` | `https://api.open-meteo.com` |
| {doc}`historical-weather` | `HistoricalWeatherClient` | `https://archive-api.open-meteo.com` |
| {doc}`air-quality` | `AirQualityClient` | `https://air-quality-api.open-meteo.com` |
| {doc}`marine` | `MarineClient` | `https://marine-api.open-meteo.com` |
| {doc}`ensemble` | `EnsembleClient` | `https://ensemble-api.open-meteo.com` |
| {doc}`seasonal` | `SeasonalClient` | `https://seasonal-api.open-meteo.com` |
| {doc}`climate` | `ClimateClient` | `https://climate-api.open-meteo.com` |
| {doc}`flood` | `FloodClient` | `https://flood-api.open-meteo.com` |
| {doc}`elevation` | `ElevationClient` | `https://api.open-meteo.com` |
| {doc}`geocoding` | `GeocodingClient` | `https://geocoding-api.open-meteo.com` |

Common to all weather services: coordinates are strings (the APIs
accept comma-separated multi-location requests), the response blocks
are parallel lists with `*_units` companions, unrequested blocks come
back `None`, and `timezone="auto"` resolves the local time zone.
Commercial subscriptions pass `apikey=` on the operations and the
`customer-`-prefixed host as the client's `base_url`.

```{toctree}
:maxdepth: 1

forecast
historical-weather
air-quality
marine
ensemble
seasonal
climate
flood
elevation
geocoding
```
