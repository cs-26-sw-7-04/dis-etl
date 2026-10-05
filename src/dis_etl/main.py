from tqdm import tqdm

import psycopg2
import pygrametl

from dis_etl.extract import get_sale_source, get_member_source
from dis_etl.datetime_dim import build_dim_datetime, get_datetime_key
from dis_etl.factsale_dim import build_fact_sale
from dis_etl.factsale_utils import fact_sale_grouped
from dis_etl.member_dim import build_member, get_member_key
pgconn = psycopg2.connect(
    dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432
)
conn = pygrametl.ConnectionWrapper(connection=pgconn)

dim_datetime = build_dim_datetime(conn)

sale_rows = list(get_sale_source())   # tqdm needs a known length for an accurate ETA/percentage

for row in tqdm(sale_rows, desc='Loading dim_datetime', unit='rows'):
    dt_key = get_datetime_key(dim_datetime, row['timestamp'])

conn.commit()

dim_member = build_member(conn)

members = list(get_member_source())

GENDER_MAP = {"M": "Male", "F": "Female", "U": "Unknown"}

for member in tqdm(members, desc="LOading dim_member", unit="rows"):
    dim_member.ensure({
        "member_id": member["id"],
        "year_joined": member["year"] if member["year"] is not None else -1,
        "gender": GENDER_MAP.get(member["gender"], "Unknown")
    })

conn.commit()

dim_facttable = build_fact_sale(conn)

groupedsale = list(fact_sale_grouped())

for row in tqdm(groupedsale, desc="Loading fact_sale", unit="rows"):

    row['dim_datetime'] = get_datetime_key(dim_datetime, row['timestamp'])
    row['dim_member'] = get_member_key(dim_member, row['member_id'])
    # 
    #row['dim_product'] = get_product_key(index, row['product_id'], row['timestamp'])
    dim_facttable.insert(row)
conn.commit()
conn.close()