import unittest
from pathlib import Path
from urllib.parse import urlsplit

from action0.client.testing import StubBackend
from action0.open_meteo.elevation import ElevationClient
from action0.open_meteo.elevation import GetV1Elevation
from action0.req import Response

FIXTURES = Path(__file__).parent / "fixtures"


class ElevationTestCase(unittest.TestCase):
    """
    tests for the elevation lookup (it shares api.open-meteo.com with
    the forecast service)
    """

    def test_request_and_parse(self) -> None:
        """
        Test the request path and the parsed elevation list.
        """
        backend = StubBackend(Response(200, body=(FIXTURES / "elevation.json").read_text()))
        client = ElevationClient(backend)

        result = client.send(GetV1Elevation(latitude="48.21", longitude="16.37"))

        url = urlsplit(backend.requests[0].url.as_str())
        self.assertEqual(url.netloc, "api.open-meteo.com")
        self.assertEqual(url.path, "/v1/elevation")
        self.assertEqual(result.elevation, [194.0])
