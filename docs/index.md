# action0-open-meteo-api

Fully typed Python clients for the [Open-Meteo](https://open-meteo.com/)
weather APIs, built on
[action0-client](https://laughinjar.github.io/action0-client/): every
endpoint is a typed operation dataclass that runs synchronously, on
asyncio or on Twisted — decided by the backend you plug in, with the
static types following along.

```shell
uv add "action0-open-meteo-api[httpx]"
```

```python
from action0.open_meteo.forecast import ForecastClient, GetV1Forecast

client = ForecastClient(RequestsBackend())
weather = client.send(GetV1Forecast(latitude="48.21", longitude="16.37"))

client = ForecastClient(AsyncHttpxBackend())
weather = await client.send(GetV1Forecast(latitude="48.21", longitude="16.37"))
```

The client code is **generated** from Open-Meteo's official OpenAPI
schemas by
[action0-client-openapi](https://laughinjar.github.io/action0-client-openapi/)
and checked in like hand-written code — this project doubles as the
generator's worked real-world example; {doc}`usage/generation` tells the
whole story.

```{toctree}
:maxdepth: 2

usage/index
api
```
