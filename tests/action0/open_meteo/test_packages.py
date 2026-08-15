import importlib
import inspect
import unittest

#: every generated subpackage with its client class and default base URL
PACKAGES = {
    "forecast": ("ForecastClient", "https://api.open-meteo.com"),
    "historical_weather": ("HistoricalWeatherClient", "https://archive-api.open-meteo.com"),
    "air_quality": ("AirQualityClient", "https://air-quality-api.open-meteo.com"),
    "marine": ("MarineClient", "https://marine-api.open-meteo.com"),
    "ensemble": ("EnsembleClient", "https://ensemble-api.open-meteo.com"),
    "seasonal": ("SeasonalClient", "https://seasonal-api.open-meteo.com"),
    "climate": ("ClimateClient", "https://climate-api.open-meteo.com"),
    "flood": ("FloodClient", "https://flood-api.open-meteo.com"),
    "elevation": ("ElevationClient", "https://api.open-meteo.com"),
    "geocoding": ("GeocodingClient", "https://geocoding-api.open-meteo.com"),
}


class GeneratedPackagesTestCase(unittest.TestCase):
    """
    smoke tests over every generated subpackage: importing the package
    runs action0-client's ``__init_subclass__`` validation of every
    operation class, so a package that imports is a package whose
    operations are well-formed
    """

    def test_packages_import_and_export(self) -> None:
        """
        Test that each subpackage imports, re-exports everything in
        ``__all__``, and its client defaults to the service's base URL.
        """
        for name, (client_name, base_url) in PACKAGES.items():
            with self.subTest(package=name):
                package = importlib.import_module(f"action0.open_meteo.{name}")
                exported = package.__all__
                self.assertIn(client_name, exported)
                for symbol in exported:
                    self.assertTrue(hasattr(package, symbol), f"{name} misses {symbol}")
                client = getattr(package, client_name)
                signature = inspect.signature(client.__init__)
                self.assertEqual(signature.parameters["base_url"].default, base_url)
