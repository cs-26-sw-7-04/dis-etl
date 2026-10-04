"""
dim_datetime setup and load logic.
"""

import pygrametl
from pygrametl.tables import CachedDimension

from dis_etl.datetime_utils import decompose_datetime


def build_dim_datetime(connection) -> CachedDimension:
    """
    a pygrametl.ConnectionWrapper wrapping a psycopg2 connection to the fklubdw database
    """
    return CachedDimension(
        name="dim_datetime",
        key="id",
        attributes=[
            "timestamp_utc",
            "year",
            "month",
            "month_name",
            "week",
            "weekday",
            "day",
            "hour",
            "minute",
            "timeslot",
            "timeslot_type",
        ],
        lookupatts=["timestamp_utc"],  # dedup / find-or-insert key
    )


def get_datetime_key(dim_datetime: CachedDimension, dt_utc) -> int:
    """
    Decompose a UTC datetime and ensure a matching dim_datetime row
    exists, returning its surrogate key.
    """
    row = decompose_datetime(dt_utc)
    return dim_datetime.ensure(row)
