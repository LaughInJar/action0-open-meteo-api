# Climate change projections

`action0.open_meteo.climate` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/climate-api) ·
`ClimateClient`, preset to `https://climate-api.open-meteo.com`

`GetV1Climate` serves downscaled CMIP6 (HighResMIP) projections from
1950 to 2050, daily resolution. `start_date` and `end_date` are
required; pick **one** climate model per request (see the note below):

```python
import datetime

from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.climate import (
    ClimateClient,
    GetV1Climate,
    GetV1ClimateDailyItem,
    GetV1ClimateModelsItem,
)

with RequestsBackend() as backend:
    client = ClimateClient(backend)
    projection = client.send(
        GetV1Climate(
            latitude="48.21",
            longitude="16.37",
            start_date=datetime.date(2040, 1, 1),
            end_date=datetime.date(2040, 12, 31),
            daily=[GetV1ClimateDailyItem.TEMPERATURE_2M_MAX],
            models=[GetV1ClimateModelsItem.MRI_AGCM3_2_S],
        )
    )

assert projection.daily is not None
print(projection.daily.temperature_2m_max[:3])  # [3.2, 5.0, 6.7]
```

## Notes

- **One model per request.** With a single entry in `models=` the API
  answers with the plain variable names the typed model declares. With
  *several* models it switches to per-model suffixed keys
  (`temperature_2m_max_MRI_AGCM3_2_S`, ...) that the upstream schema
  does not declare — those keys are dropped by the generated model, so
  comparing models means one request per model. (Upstream schema gap;
  tracked in `schemas/README.md`.)
- Projections show climate, not weather: analyze distributions over
  years, never a single simulated day.
- `disable_bias_correction=True` returns the raw model output.
