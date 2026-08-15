# Elevation

`action0.open_meteo.elevation` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/elevation-api) ·
`ElevationClient`, preset to `https://api.open-meteo.com` (shared with
the forecast service)

`GetV1Elevation` resolves coordinates to terrain elevation from a
90-metre digital elevation model (Copernicus GLO-90). `latitude` and
`longitude` take comma-separated lists, so one request resolves up to
100 points:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.elevation import ElevationClient, GetV1Elevation

with RequestsBackend() as backend:
    client = ElevationClient(backend)
    result = client.send(GetV1Elevation(latitude="48.21,47.07", longitude="16.37,15.44"))

print(result.elevation)  # [194.0, 357.0] — Vienna, Graz
```

## Notes

- The answer's `elevation` list is index-aligned with the coordinates
  you sent.
- The weather APIs already resolve elevation internally (and accept an
  `elevation=` override) — call this API when you need the number
  itself.
