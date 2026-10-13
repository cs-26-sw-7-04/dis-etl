"""
dim_datetime setup and load logic.
"""

from pygrametl.tables import CachedBulkDimension

from dis_etl.datetime_utils import decompose_datetime

DATETIME_CACHE_SIZE = 100000


def build_dim_datetime(connection) -> CachedBulkDimension:
    """
    a pygrametl.ConnectionWrapper wrapping a psycopg2 connection to the fklubdw database
    """
    def pgbulkloader(name, attributes, fieldsep, rowsep, nullval, filehandle):
        filehandle.seek(0)
        with connection.cursor() as cursor:
            cursor.copy_from(
                file=filehandle,
                table=name,
                sep=fieldsep,
                null=str(nullval),
                columns=attributes,
            )

    return CachedBulkDimension(
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
        lookupatts=["timestamp_utc"],
        bulkloader=pgbulkloader,
        cachesize=DATETIME_CACHE_SIZE,
        targetconnection=connection,
    )


def get_datetime_key(dim_datetime: CachedBulkDimension, dt_utc) -> int:
    """
    Decompose a UTC datetime and ensure a matching dim_datetime row
    exists, returning its surrogate key.
    """
    row = decompose_datetime(dt_utc)
    return dim_datetime.ensure(row)
