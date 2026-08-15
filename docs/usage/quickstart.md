# Quickstart

Install the package together with the HTTP library your backend needs —
the extras mirror
[action0-client's backends](https://laughinjar.github.io/action0-client/usage/backends.html)
(`requests`, `httpx`, `aiohttp`, `urllib3`, `twisted`; the urllib and
thread-pool backends are stdlib-only and need no extra):

```shell
uv add "action0-open-meteo-api[httpx]"
```

## From place name to forecast

Each Open-Meteo service has a subpackage of its own with a client preset
to the service's base URL. Turn a place name into coordinates with the
geocoding service, then ask the forecast service for the weather:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.forecast import ForecastClient, GetV1Forecast, GetV1ForecastHourlyItem
from action0.open_meteo.geocoding import GeocodingClient, SearchLocations

with RequestsBackend() as backend:
    places = GeocodingClient(backend)  # https://geocoding-api.open-meteo.com
    found = places.send(SearchLocations(name="Vienna", count=1))
    assert found.results, "no place matched"
    vienna = found.results[0]  # Location(id=2761369, name="Vienna", ...)

    weather = ForecastClient(backend)  # https://api.open-meteo.com
    forecast = weather.send(
        GetV1Forecast(
            latitude=str(vienna.latitude),
            longitude=str(vienna.longitude),
            hourly=[GetV1ForecastHourlyItem.TEMPERATURE_2M, GetV1ForecastHourlyItem.RAIN],
            forecast_days=1,
        )
    )
    assert forecast.hourly is not None
    print(forecast.hourly.time)  # ["2026-08-15T00:00", "2026-08-15T01:00", ...]
    print(forecast.hourly.temperature_2m)  # [17.2, 16.8, ...]
```

The weather variables are generated enums, so your IDE completes the
legal values; dates (`start_date=`, `end_date=`) are `datetime.date`;
the responses are plain typed dataclasses. Fields you did not request
come back as `None`.

## Sync, async or Twisted — the backend decides

The clients are generic over the backend, so the execution model is
your choice, with the static types following along:

```python
from action0.client.backends.httpx import AsyncHttpxBackend

async with AsyncHttpxBackend() as backend:
    weather = ForecastClient(backend)
    forecast = await weather.send(GetV1Forecast(latitude="48.21", longitude="16.37"))
```

Non-2xx responses raise `action0.client.APIError` with request and
response attached; transport problems arrive as `TransportError` /
`TimeoutError` — see the
[action0-client error guide](https://laughinjar.github.io/action0-client/usage/errors.html).

## No API key needed (usually)

The Open-Meteo APIs are free for non-commercial use without any key
([terms](https://open-meteo.com/en/terms)). Commercial subscriptions
pass their key in the operations' `apikey` field and the
`customer-`-prefixed hosts as the client's `base_url`:

```python
weather = ForecastClient(backend, base_url="https://customer-api.open-meteo.com")
forecast = weather.send(GetV1Forecast(latitude="48.21", longitude="16.37", apikey="..."))
```

## Testing your integration

The stub backends of `action0.client.testing` drive the clients without
a server — exactly how this repository tests the generated packages
(`examples/vienna_forecast.py` is a complete network-free demo):

```python
from action0.client.testing import StubBackend
from action0.req import Response

backend = StubBackend(Response(200, body='{"elevation": [194.0]}'))
client = ElevationClient(backend)
print(client.send(GetV1Elevation(latitude="48.21", longitude="16.37")).elevation)  # [194.0]
print(backend.requests[0].url.as_str())  # the URL that would have been fetched
```
