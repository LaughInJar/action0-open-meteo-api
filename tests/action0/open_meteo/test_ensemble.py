import unittest
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlsplit

from action0.client.testing import StubBackend
from action0.open_meteo.ensemble import EnsembleClient
from action0.open_meteo.ensemble import GetV1Ensemble
from action0.open_meteo.ensemble import GetV1EnsembleHourlyItem
from action0.open_meteo.ensemble import GetV1EnsembleModelsItem
from action0.req import Response

FIXTURES = Path(__file__).parent / "fixtures"


class EnsembleTestCase(unittest.TestCase):
    """
    tests for the ensemble operations — the API answering with dynamic
    per-member keys (``temperature_2m_member01``, ...), which land in
    the models' catch-all ``additional_properties`` field
    """

    def test_member_variables_land_in_the_catch_all(self) -> None:
        """
        Test that the declared ``time`` field parses normally while the
        dynamic member variables are collected, typed.
        """
        backend = StubBackend(Response(200, body=(FIXTURES / "ensemble.json").read_text()))
        client = EnsembleClient(backend)

        result = client.send(
            GetV1Ensemble(
                latitude="48.21",
                longitude="16.37",
                hourly=[GetV1EnsembleHourlyItem.TEMPERATURE_2M],
                models=[GetV1EnsembleModelsItem.DWD_ICON_SEAMLESS_EPS],
                forecast_days=1,
            )
        )

        url = urlsplit(backend.requests[0].url.as_str())
        self.assertEqual(url.netloc, "ensemble-api.open-meteo.com")
        self.assertEqual(url.path, "/v1/ensemble")
        self.assertEqual(parse_qs(url.query)["models"], ["dwd_icon_seamless_eps"])

        hourly = result.hourly
        assert hourly is not None
        assert hourly.time is not None
        self.assertEqual(len(hourly.time), 24)
        extras = hourly.additional_properties
        assert extras is not None
        # the ensemble mean plus every member arrives as a dynamic key
        self.assertIn("temperature_2m", extras)
        self.assertIn("temperature_2m_member01", extras)
        member = extras["temperature_2m_member01"]
        self.assertEqual(len(member), 24)
        self.assertIsInstance(member[0], float)
        # declared properties stay out of the catch-all
        self.assertNotIn("time", extras)
        units = result.hourly_units
        assert units is not None and units.additional_properties is not None
        self.assertEqual(units.additional_properties["temperature_2m"], "°C")
