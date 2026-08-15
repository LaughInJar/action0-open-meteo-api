"""
Geocoding a city and fetching its weather forecast, in every execution
model: the same :py:class:`~action0.open_meteo.geocoding.SearchLocations`
and :py:class:`~action0.open_meteo.forecast.GetV1Forecast` operations,
driven synchronously, with asyncio, or with Twisted — only the backend
changes.

Run it (no network involved, the demo uses the stub backend)::

    uv run python examples/vienna_forecast.py
"""

from __future__ import annotations

from action0.open_meteo.forecast import ForecastClient
from action0.open_meteo.forecast import GetV1Forecast
from action0.open_meteo.forecast import GetV1ForecastCurrentItem
from action0.open_meteo.forecast import GetV1ForecastHourlyItem
from action0.open_meteo.forecast import GetV1ForecastResponse
from action0.open_meteo.geocoding import GeocodingClient
from action0.open_meteo.geocoding import SearchLocations


def sync_usage() -> None:
    """The clients with the (sync) requests backend."""
    from action0.client.backends.requests import RequestsBackend

    with RequestsBackend() as backend:
        places = GeocodingClient(backend)
        found = places.send(SearchLocations(name="Vienna", count=1))
        assert found.results, "no place matched"
        vienna = found.results[0]

        weather = ForecastClient(backend)
        forecast: GetV1ForecastResponse = weather.send(
            GetV1Forecast(
                latitude=str(vienna.latitude),
                longitude=str(vienna.longitude),
                hourly=[GetV1ForecastHourlyItem.TEMPERATURE_2M],
                forecast_days=1,
            )
        )
        assert forecast.hourly is not None
        print(forecast.hourly.temperature_2m)


async def async_usage() -> None:
    """The same operations with the async httpx backend."""
    from action0.client.backends.httpx import AsyncHttpxBackend

    async with AsyncHttpxBackend() as backend:
        weather = ForecastClient(backend)
        forecast = await weather.send(
            GetV1Forecast(latitude="48.21", longitude="16.37", forecast_days=1)
        )
        print(forecast.current)


# ---------------------------------------------------------------------------
# A runnable, network-free demo: the stub backend answers instead of the
# Open-Meteo servers — which is also exactly how an application would
# test its own weather code.


def demo() -> None:
    """Exercise both clients against canned responses and print the results."""
    from action0.client.testing import StubBackend
    from action0.req import Response

    geocoding_payload = """{
        "results": [{
            "id": 2761369, "name": "Vienna", "latitude": 48.20849, "longitude": 16.37208,
            "elevation": 171.0, "country_code": "AT", "country": "Austria",
            "timezone": "Europe/Vienna", "population": 1691468
        }],
        "generationtime_ms": 0.4
    }"""
    forecast_payload = """{
        "latitude": 48.2, "longitude": 16.38, "elevation": 186.0,
        "timezone": "GMT", "utc_offset_seconds": 0,
        "current_units": {"time": "iso8601", "temperature_2m": "\\u00b0C", "weather_code": "wmo code"},
        "current": {"time": "2026-08-15T12:00", "interval": 900,
                    "temperature_2m": 24.3, "weather_code": 3},
        "hourly_units": {"time": "iso8601", "temperature_2m": "\\u00b0C"},
        "hourly": {"time": ["2026-08-15T00:00", "2026-08-15T01:00"],
                   "temperature_2m": [17.2, 16.8]}
    }"""
    backend = StubBackend(
        Response(200, body=geocoding_payload),
        Response(200, body=forecast_payload),
    )

    # place name -> coordinates
    places = GeocodingClient(backend)
    found = places.send(SearchLocations(name="Vienna", count=1))
    assert found.results is not None
    vienna = found.results[0]
    print(f"{vienna.name}, {vienna.country}: {vienna.latitude}, {vienna.longitude}")

    # coordinates -> forecast; the weather variables are enums, so IDE
    # completion knows the legal values
    weather = ForecastClient(backend)
    forecast = weather.send(
        GetV1Forecast(
            latitude=str(vienna.latitude),
            longitude=str(vienna.longitude),
            hourly=[GetV1ForecastHourlyItem.TEMPERATURE_2M],
            current=[
                GetV1ForecastCurrentItem.TEMPERATURE_2M,
                GetV1ForecastCurrentItem.WEATHER_CODE,
            ],
            forecast_days=1,
        )
    )
    assert forecast.current is not None and forecast.hourly is not None
    print(f"now: {forecast.current.temperature_2m} °C (wmo {forecast.current.weather_code})")
    print(f"hourly: {forecast.hourly.temperature_2m}")

    print("requests sent:")
    for request in backend.requests:
        print("  ", request.method, request.url.as_str())


if __name__ == "__main__":
    demo()
