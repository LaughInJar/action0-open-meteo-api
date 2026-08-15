# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`action0-open-meteo-api` ships fully typed clients for the [Open-Meteo](https://open-meteo.com/) APIs, built on [`action0-client`](https://github.com/LaughInJar/action0-client) — operations run synchronously, on asyncio or on Twisted, decided by the plugged-in backend. The client code is **generated** by [`action0-client-openapi`](https://github.com/LaughInJar/action0-client-openapi) from the OpenAPI schemas vendored in `schemas/` and checked in; the project doubles as that generator's worked real-world example (purpose three: `docs/usage/generation.md` documents exactly how the code was generated). It ships the `action0.open_meteo` package (`action0` is a PEP 420 namespace package) from a `src/` layout, is built with hatchling, and uses `uv`. Runtime dependencies are `action0-client`, `action0-req` and `action0-url`; the HTTP libraries come in through `action0-client`'s optional extras, mirrored here as extras of the same names; `action0-client-openapi[yaml]` is a dev dependency for regeneration only — the shipped code never imports it.

## Rules

- **Never commit without asking.** Also never push, tag, or publish on your own.
- **Branches + PRs.** All changes go through feature branches and GitHub pull requests that Simon reviews and merges — never commit to `main` directly. (Only the initial project scaffold was built directly on `main`; that phase is over.)
- **Discuss first.** Always present the plan and the intended edits and get agreement before changing files.
- **Never hand-edit the generated packages** (`src/action0/open_meteo/<service>/` — everything with a `do not edit` header). Fix the schema in `schemas/` or the generator itself, then run `bash tools/regenerate.sh` and review the diff. Generator shortcomings discovered here are fixed in action0-client-openapi, not worked around here.
- Every (hand-written) code change comes with: tests, docstrings, inline comments where the code isn't self-explanatory, and updated usage examples in `README.md` and the Sphinx docs (the guide pages in `docs/usage/`).
- Before considering work done, run ruff, mypy, pyright, ty, and pytest (commands below) and fix what they report.
- Supported Python versions: 3.11 up to the latest release. Don't use syntax or stdlib features introduced after 3.11, and don't rely on behavior removed in newer versions.

## Commands

`uv run` syncs the environment automatically (the dev dependency group, which includes the generator and all optional backend libraries, is installed by default), so no separate install step is needed.

```sh
uv run pytest                                        # all tests
uv run pytest tests/action0/open_meteo/test_forecast.py  # one file

uv run ruff check      # lint (add --fix to autofix)
uv run ruff format     # format
uv run mypy            # type-check (strict; files are configured in pyproject.toml)
uv run pyright         # type-check
uv run ty check        # type-check

bash tools/regenerate.sh   # regenerate all subpackages from schemas/

uv run python examples/vienna_forecast.py  # the network-free demo (CI runs it)

uv run --group docs sphinx-build -W --keep-going -b html docs docs/_build/html  # build docs

uv build               # build sdist + wheel into dist/
```

## Architecture

- `schemas/` — the OpenAPI documents. Nine are vendored verbatim from [open-meteo/open-meteo](https://github.com/open-meteo/open-meteo)'s `openapi/` directory (`schemas/README.md` pins the upstream commit); `geocoding.yml` is authored by this project (upstream publishes none) against the API docs and live responses.
- `tools/regenerate.sh` — one `action0-openapi` run per schema into `src/action0/open_meteo/`, with `--package-name`/`--client-name` overriding the title-derived defaults. Base URLs come from the schemas' path-level `servers` (the generator's fallback), so no `--base-url` flags.
- `src/action0/open_meteo/__init__.py` — hand-written package root: docstring, single-sourced `__version__` (hatch extracts it via the regex in `[tool.hatch.version]`; bump only there), no re-exports — users import from the service subpackages. `py.typed` sits next to it.
- `src/action0/open_meteo/<service>/` — the ten generated subpackages (forecast, historical_weather, air_quality, marine, ensemble, seasonal, climate, flood, elevation, geocoding), each `client.py` + `operations.py` + `models.py` + re-exporting `__init__.py` + `py.typed`. Notable generated shapes: weather variables are enum lists (`hourly=[GetV1ForecastHourlyItem.TEMPERATURE_2M]`, serialized as repeated query params — Open-Meteo merges them like its documented comma form); ensemble/seasonal member variables arrive as dynamic JSON keys and land in the models' catch-all `additional_properties` dict; `latitude`/`longitude` are `str` because the schema allows comma-separated multi-coordinate requests; elevation shares `api.open-meteo.com` with forecast.
- `tests/action0/open_meteo/` — `unittest.TestCase` via pytest, network-free: `StubBackend` plays back captured live payloads from `tests/action0/open_meteo/fixtures/*.json` (refresh by re-running the curl commands in the git history if the API shape drifts). `test_packages.py` smoke-imports every subpackage (import runs action0-client's `__init_subclass__` validation of every operation) and pins each client's default base URL.
- `examples/vienna_forecast.py` — the complete worked example (geocode → forecast; sync/async variants plus a StubBackend demo; type-checked via mypy's `files`, runnable without network — CI runs it).
- Releases: pushing a `vX.Y.Z` tag triggers `.github/workflows/release.yml` (re-runs all checks, verifies the tag matches `__version__`, builds, publishes to PyPI via trusted publishing, environment `pypi`). Never bump the version, tag, or publish on your own — releasing is the user's call.
- Docs: Sphinx + Furo + MyST in `docs/`, autodoc over the generated modules for the API reference; CI builds with `-W` and deploys to GitHub Pages on pushes to `main`. Guide pages in `docs/usage/` (quickstart, per-API tour in `apis.md`, and `generation.md` — the "how this was generated" story; keep it truthful when regenerating). Ruff enforces one import per line (isort `force-single-line`), line length 99, `action0` first-party.
