# dis-etl

ETL pipeline loading CSV data into a Postgres warehouse via pygrametl.

## Setup

```sh
$ docker compose up -d   # starts Postgres + pgAdmin
```

## Run

**mise + uv**
```sh
mise install
uv run dis-etl
```

**uv only**
```sh
uv run dis-etl
```

**plain Python**
```sh
pip install .
dis-etl
```

## Shut down Postgres + pgAdmin docker compose

```sh
$ docker compose down
```
