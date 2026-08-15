import unittest
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlsplit

from action0.client import APIError
from action0.client.testing import StubBackend
from action0.open_meteo.forecast import BadRequestError
from action0.open_meteo.forecast import ForecastClient
from action0.open_meteo.forecast import GetV1Forecast
from action0.open_meteo.forecast import GetV1ForecastCurrentItem
from action0.open_meteo.forecast import GetV1ForecastHourlyItem
from action0.req import Response

FIXTURES = Path(__file__).parent / "fixtures"


class ForecastTestCase(unittest.TestCase):
    """
    tests for the forecast operations against a captured live payload
    (tests/action0/open_meteo/fixtures/forecast.json — no network)
    """

    def test_request_and_parse(self) -> None:
        """
        Test both wire directions: the query the operation builds, and
        the payload parsing into the typed response.
        """
        backend = StubBackend(Response(200, body=(FIXTURES / "forecast.json").read_text()))
        client = ForecastClient(backend)

        weather = client.send(
            GetV1Forecast(
                latitude="48.21",
                longitude="16.37",
                hourly=[GetV1ForecastHourlyItem.TEMPERATURE_2M, GetV1ForecastHourlyItem.RAIN],
                current=[
                    GetV1ForecastCurrentItem.TEMPERATURE_2M,
                    GetV1ForecastCurrentItem.WEATHER_CODE,
                ],
                forecast_days=1,
            )
        )

        url = urlsplit(backend.requests[0].url.as_str())
        self.assertEqual(url.netloc, "api.open-meteo.com")
        self.assertEqual(url.path, "/v1/forecast")
        query = parse_qs(url.query)
        self.assertEqual(query["latitude"], ["48.21"])
        self.assertEqual(query["longitude"], ["16.37"])
        # the schema declares explode: false, so the enum lists join
        # into one comma-separated pair — Open-Meteo's documented form
        self.assertEqual(query["hourly"], ["temperature_2m,rain"])
        self.assertEqual(query["current"], ["temperature_2m,weather_code"])
        self.assertEqual(query["forecast_days"], ["1"])
        # enum-typed defaults go out as their wire values too
        self.assertEqual(query["temperature_unit"], ["celsius"])

        assert weather.hourly is not None
        assert weather.hourly.time is not None
        assert weather.hourly.temperature_2m is not None
        assert weather.hourly.rain is not None
        self.assertEqual(len(weather.hourly.time), 24)
        self.assertEqual(len(weather.hourly.temperature_2m), 24)
        self.assertIsInstance(weather.hourly.temperature_2m[0], float)
        assert weather.current is not None
        self.assertIsInstance(weather.current.temperature_2m, float)
        self.assertIsInstance(weather.current.weather_code, int)
        assert weather.hourly_units is not None
        self.assertEqual(weather.hourly_units.temperature_2m, "°C")
        self.assertEqual(weather.timezone, "GMT")

    def test_documented_400_raises_typed_error(self) -> None:
        """
        Test that the documented 400 answer raises the generated
        BadRequestError carrying Open-Meteo's parsed error payload
        (still an APIError, so broad handlers keep working).
        """
        body = '{"error": true, "reason": "Latitude must be in range of -90 to 90"}'
        backend = StubBackend(Response(400, body=body))
        client = ForecastClient(backend)
        with self.assertRaises(BadRequestError) as caught:
            client.send(GetV1Forecast(latitude="91", longitude="16.37"))
        self.assertIsInstance(caught.exception, APIError)
        self.assertTrue(caught.exception.error.error)
        self.assertEqual(caught.exception.error.reason, "Latitude must be in range of -90 to 90")

    def test_unparsable_error_body_stays_plain_apierror(self) -> None:
        """
        Test that a non-JSON 400 body falls back to the plain APIError.
        """
        backend = StubBackend(Response(400, body=b"<html>bad</html>"))
        client = ForecastClient(backend)
        with self.assertRaises(APIError) as caught:
            client.send(GetV1Forecast(latitude="91", longitude="16.37"))
        self.assertNotIsInstance(caught.exception, BadRequestError)
