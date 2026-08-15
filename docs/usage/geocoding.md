# Geocoding

`action0.open_meteo.geocoding` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/geocoding-api) ·
`GeocodingClient`, preset to `https://geocoding-api.open-meteo.com`

`SearchLocations` turns a place name (or postal code) into ranked
`Location` results with the coordinates every other Open-Meteo API
wants; `GetLocation` looks a single location up by its GeoNames id:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.geocoding import GeocodingClient, GetLocation, SearchLocations

with RequestsBackend() as backend:
    client = GeocodingClient(backend)

    found = client.send(SearchLocations(name="Vienna", count=3, language="de"))
    assert found.results, "no place matched"
    for place in found.results:
        print(place.name, place.country_code, place.latitude, place.longitude)
    # Wien AT 48.20849 16.37208
    # Vienna US 32.09156 -83.79545
    # ...

    vienna = client.send(GetLocation(id=2761369))
    print(vienna.timezone, vienna.population)  # Europe/Vienna 1691468
```

## Notes

- Two-character queries match exactly, three or more match fuzzily;
  results are ranked by population. **No match means `results` is
  `None`**, not an empty list — the API omits the key.
- `language=` translates the returned names where a translation exists
  (`"de"` turns Vienna into Wien); it defaults to `"en"`.
- A `Location` carries the administrative hierarchy (`admin1` ...
  `admin4` with their GeoNames ids), `postcodes`, `elevation` and
  `timezone` — the latter pairs nicely with the weather APIs'
  `timezone=` parameter.
- This is the one Open-Meteo service without an upstream OpenAPI
  schema — `schemas/geocoding.yml` is written by this project
  ({doc}`generation` tells that story).
