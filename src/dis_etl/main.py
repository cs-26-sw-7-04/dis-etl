from tqdm import tqdm

import psycopg2
import pygrametl

from dis_etl.extract import get_sale_source
from dis_etl.datetime_dim import build_dim_datetime, get_datetime_key

pgconn = psycopg2.connect(
    dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432
)
conn = pygrametl.ConnectionWrapper(connection=pgconn)

dim_datetime = build_dim_datetime(conn)

sale_rows = list(get_sale_source())   # tqdm needs a known length for an accurate ETA/percentage

for row in tqdm(sale_rows, desc='Loading dim_datetime', unit='rows'):
    dt_key = get_datetime_key(dim_datetime, row['timestamp'])

conn.commit()
conn.close()
