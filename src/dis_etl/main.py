"""Main entrypoint"""

import psycopg2
import pygrametl
from tqdm import tqdm
from dis_etl.product_dim import build_dim_product, get_product_key, lookup_product_key

from dis_etl.datetime_dim import build_dim_datetime, get_datetime_key
from dis_etl.extract import get_member_source, get_oldprice_source, get_sale_source, get_product_source
from dis_etl.member_dim import (
    build_dim_member,
    get_member_key,
    lookup_member_key,
    unknown_member_row,
)
from dis_etl.sale_fact_table import (
    PLACEHOLDER_PRODUCT_KEY,
    build_fact_table_sale,
    fact_sale_grouped,
)

import datetime as dt

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

    # Update datetime dimenstion from sales, oldprice table rows

    dim_datetime = build_dim_datetime(conn)

    sale_rows = list(
        get_sale_source()
    )  # tqdm needs a known length for an accurate ETA/percentage

    for i, raw_row in enumerate(
        tqdm(sale_rows, desc="Loading dim_datetime from sales", unit="rows")
    ):
        get_datetime_key(dim_datetime, raw_row["timestamp"])

        if (i + 1) % BATCH_SIZE == 0:
            conn.commit()

    oldprice_rows = list(
        get_oldprice_source()
    )  # tqdm needs a known length for an accurate ETA/percentage

    for i, raw_row in enumerate(
        tqdm(oldprice_rows, desc="Loading dim_datetime from oldprice", unit="rows")
    ):
        get_datetime_key(dim_datetime, raw_row["changed_on"])

        if (i + 1) % BATCH_SIZE == 0:
            conn.commit()

    conn.commit()

    dim_product = build_dim_product(conn);
    product_rows = list(get_product_source());
    for i, raw_row in enumerate(tqdm(product_rows, desc="Loading dim_product", unit="rows")):
        get_product_key(dim_product, oldprice_rows, raw_row)

        if (i + 1) % BATCH_SIZE == 0:
            conn.commit()
    conn.commit()
        

    # Update member dimention from member table rows
    dim_member = build_dim_member(conn)

    member_rows = list(get_member_source())

    for i, raw_row in enumerate(
        tqdm(member_rows, desc="Loading dim_member", unit="rows")
    ):
        get_member_key(dim_member, raw_row)

        if (i + 1) % BATCH_SIZE == 0:
            conn.commit()

    dim_member.ensure(unknown_member_row())

    conn.commit()

    # Update sales fact-table

    dim_facttable = build_fact_table_sale(conn)

    groupedsale = list(fact_sale_grouped())

    #print(f"An example product is {lookup_product_key(dim_product, 1, dt.datetime.now().replace(tzinfo=dt.timezone(dt.timedelta(0))))}")

    for row in tqdm(groupedsale, desc="Loading fact_sale", unit="rows"):
        row["dim_datetime"] = get_datetime_key(dim_datetime, row["timestamp"])
        row["dim_member"] = lookup_member_key(dim_member, row["member_id"])
        #print(f"Timestamp: {row['timestamp']}")
        row["dim_product"] = (
            lookup_product_key(dim_product, row['product_id'], row['timestamp'])
        )
        #print(f"Inserting product {row["dim_product"]} bought on {row["dim_datetime"]}")
        # TODO: Product key needs to reference the correct dim_product if price changed in
        # sales minute of multiple sales
        dim_facttable.insert(row)

    conn.commit()


if __name__ == "__main__":
    main()
