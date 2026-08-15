# Ensemble forecasts

`action0.open_meteo.ensemble` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/ensemble-api) ·
`EnsembleClient`, preset to `https://ensemble-api.open-meteo.com`

`GetV1Ensemble` returns *every member* of an ensemble model run —
dozens of slightly perturbed forecasts whose spread quantifies the
uncertainty. The members arrive as dynamic JSON keys
(`temperature_2m_member01`, ...), which land in the response models'
typed catch-all field `additional_properties`:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.ensemble import (
    EnsembleClient,
    GetV1Ensemble,
    GetV1EnsembleHourlyItem,
    GetV1EnsembleModelsItem,
)

with RequestsBackend() as backend:
    client = EnsembleClient(backend)
    runs = client.send(
        GetV1Ensemble(
            latitude="48.21",
            longitude="16.37",
            hourly=[GetV1EnsembleHourlyItem.TEMPERATURE_2M],
            models=[GetV1EnsembleModelsItem.DWD_ICON_SEAMLESS_EPS],
            forecast_days=1,
        )
    )

hourly = runs.hourly
assert hourly is not None and hourly.additional_properties is not None
members = {
    key: series
    for key, series in hourly.additional_properties.items()
    if key.startswith("temperature_2m_member")
}
print(len(members))  # 39 (ICON EPS)
noon = [series[12] for series in members.values()]
print(min(noon), max(noon))  # the uncertainty band at noon
```

## Notes

- `hourly.time` is a regular declared field; everything else —
  the control run (`temperature_2m`) and each `..._memberNN` — sits in
  `additional_properties: dict[str, list[float]]`, with the units in
  `hourly_units.additional_properties`.
- `models=` is required practically: each entry is a specific ensemble
  system (`DWD_ICON_SEAMLESS_EPS`, `ECMWF_IFS025_ENSEMBLE`, ...), and the
  member count depends on it.
- Ensemble payloads are large — request only the variables and days
  you need.
