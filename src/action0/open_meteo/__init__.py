"""
Fully typed `Open-Meteo <https://open-meteo.com/>`_ API clients built on
`action0-client <https://laughinjar.github.io/action0-client/>`_.

Each Open-Meteo service lives in a subpackage of its own, generated from
the official OpenAPI schema (the geocoding one is written by this
project — upstream publishes none) by `action0-client-openapi
<https://laughinjar.github.io/action0-client-openapi/>`_: a client class
preset to the service's base URL, one operation class per endpoint, and
the models their JSON answers are parsed into.

>>> from action0.open_meteo import forecast
>>> forecast.ForecastClient  # doctest: +ELLIPSIS
<class 'action0.open_meteo.forecast.client.ForecastClient'>

The subpackages: :py:mod:`~action0.open_meteo.forecast`,
:py:mod:`~action0.open_meteo.historical_weather`,
:py:mod:`~action0.open_meteo.air_quality`,
:py:mod:`~action0.open_meteo.marine`,
:py:mod:`~action0.open_meteo.ensemble`,
:py:mod:`~action0.open_meteo.seasonal`,
:py:mod:`~action0.open_meteo.climate`,
:py:mod:`~action0.open_meteo.flood`,
:py:mod:`~action0.open_meteo.elevation` and
:py:mod:`~action0.open_meteo.geocoding`.
"""

__version__: str = "0.1.0"
