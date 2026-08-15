#!/usr/bin/env bash
# Regenerate every action0.open_meteo subpackage from the schemas in
# schemas/ using action0-client-openapi (a dev dependency, so plain
# `uv run` finds it). Run from the repository root:
#
#     bash tools/regenerate.sh
#
# The generated packages are checked in; review the diff after
# regenerating like any other change (docs/usage/generation.md tells
# the whole story).
set -euo pipefail
cd "$(dirname "$0")/.."

generate() {
    local schema="$1" package="$2" client="$3"
    uv run action0-openapi "schemas/${schema}" \
        -o src/action0/open_meteo \
        --package-name "${package}" \
        --client-name "${client}" \
        --force
}

generate forecast.yml           forecast           ForecastClient
generate historical-weather.yml historical_weather HistoricalWeatherClient
generate air-quality.yml        air_quality        AirQualityClient
generate marine.yml             marine             MarineClient
generate ensemble.yml           ensemble           EnsembleClient
generate seasonal.yml           seasonal           SeasonalClient
generate climate.yml            climate            ClimateClient
generate flood.yml              flood              FloodClient
generate elevation.yml          elevation          ElevationClient
generate geocoding.yml          geocoding          GeocodingClient
