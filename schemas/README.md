# The OpenAPI schemas

The nine weather schemas are vendored verbatim from the
[open-meteo/open-meteo](https://github.com/open-meteo/open-meteo)
repository's `openapi/` directory, at commit
[`5fcb532`](https://github.com/open-meteo/open-meteo/tree/5fcb53297b1726692e9b8aaf5aaba921168b67cb/openapi)
(fetched 2026-08-15). They are licensed by Open-Meteo under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

`geocoding.yml` is **not** from upstream — Open-Meteo publishes no
OpenAPI document for the Geocoding API. It was written for this project
against the [Geocoding API docs](https://open-meteo.com/en/docs/geocoding-api)
and verified against live responses.

To refresh the vendored schemas, download the `openapi/*.yml` files from
upstream `main`, update the commit hash above, then regenerate the
subpackages (`bash tools/regenerate.sh`) and review the diff.
