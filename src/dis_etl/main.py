"""Main entrypoint"""

import psycopg2
import pygrametl
from tqdm import tqdm

from dis_etl.datetime_dim import build_dim_datetime, get_datetime_key
from dis_etl.extract import get_member_source, get_sale_source
from dis_etl.member_dim import build_dim_member, get_member_key
from dis_etl.sale_fact_table import build_fact_table_sale, fact_sale_grouped

BATCH_SIZE = 2000


def main() -> None:
    """Main entrypoint for program ocestrating ETL from Fklub data tables to fklubdw"""
    pgconn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432,
    )
    conn = pygrametl.ConnectionWrapper(connection=pgconn)

    # Update datetime dimenstion from sales table rows

    dim_datetime = build_dim_datetime(conn)

    sale_rows = list(
        get_sale_source()
    )  # tqdm needs a known length for an accurate ETA/percentage

    for i, raw_row in enumerate(tqdm(sale_rows, desc="Loading dim_datetime", unit="rows")):
        get_datetime_key(dim_datetime, raw_row["timestamp"])

        if (i + 1) % BATCH_SIZE == 0:
            conn.commit()

    conn.commit()

    # Update member dimention from member table rows

    dim_member = build_dim_member(conn)

    member_rows = list(get_member_source())

    for i, raw_row in enumerate(tqdm(member_rows, desc="Loading dim_member", unit="rows")):
        get_member_key(dim_member, raw_row)

        if (i + 1) % BATCH_SIZE == 0:
            conn.commit()

    conn.commit()

    # Update sales fact-table

    dim_facttable = build_fact_table_sale(conn)

    groupedsale = list(fact_sale_grouped())

    for row in tqdm(groupedsale, desc="Loading fact_sale", unit="rows"):
        row["dim_datetime"] = get_datetime_key(dim_datetime, row["timestamp"])
        row["dim_member"] = get_member_key(dim_member, row["member_id"])
        # row['dim_product'] = get_product_key(index, row['product_id'], row['timestamp'])
        dim_facttable.insert(row)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
