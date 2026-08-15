import json
import unittest
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlsplit

from action0.client.testing import StubBackend
from action0.open_meteo.geocoding import GeocodingClient
from action0.open_meteo.geocoding import GetLocation
from action0.open_meteo.geocoding import Location
from action0.open_meteo.geocoding import SearchLocations
from action0.req import Response

FIXTURES = Path(__file__).parent / "fixtures"


class SearchLocationsTestCase(unittest.TestCase):
    """
    tests for the geocoding search against a captured live payload
    """

    def test_request_and_parse(self) -> None:
        """
        Test the search request and the parsed result list.
        """
        backend = StubBackend(Response(200, body=(FIXTURES / "geocoding.json").read_text()))
        client = GeocodingClient(backend)

        found = client.send(SearchLocations(name="Vienna", count=2))

        url = urlsplit(backend.requests[0].url.as_str())
        self.assertEqual(url.netloc, "geocoding-api.open-meteo.com")
        self.assertEqual(url.path, "/v1/search")
        query = parse_qs(url.query)
        self.assertEqual(query["name"], ["Vienna"])
        self.assertEqual(query["count"], ["2"])
        self.assertEqual(query["language"], ["en"])

        assert found.results is not None
        self.assertEqual(len(found.results), 2)
        vienna = found.results[0]
        self.assertIsInstance(vienna, Location)
        self.assertEqual(vienna.name, "Vienna")
        self.assertEqual(vienna.country_code, "AT")
        self.assertEqual(vienna.id, 2761369)
        self.assertAlmostEqual(vienna.latitude, 48.20849)
        self.assertEqual(vienna.timezone, "Europe/Vienna")
        assert vienna.postcodes is not None
        self.assertIn("1010", vienna.postcodes)

    def test_no_match_has_no_results(self) -> None:
        """
        Test that the results-free "nothing matched" answer parses.
        """
        backend = StubBackend(Response(200, body='{"generationtime_ms": 0.1}'))
        client = GeocodingClient(backend)
        found = client.send(SearchLocations(name="Xqzzy"))
        self.assertIsNone(found.results)


class GetLocationTestCase(unittest.TestCase):
    """
    tests for the by-id lookup
    """

    def test_request_and_parse(self) -> None:
        """
        Test that /v1/get answers with a single bare location.
        """
        payload = json.loads((FIXTURES / "geocoding.json").read_text())["results"][0]
        backend = StubBackend(Response(200, body=json.dumps(payload)))
        client = GeocodingClient(backend)

        vienna = client.send(GetLocation(id=2761369))

        url = urlsplit(backend.requests[0].url.as_str())
        self.assertEqual(url.path, "/v1/get")
        self.assertEqual(parse_qs(url.query)["id"], ["2761369"])
        self.assertEqual(vienna.name, "Vienna")
        self.assertEqual(vienna.country, "Austria")
