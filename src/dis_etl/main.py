import psycopg2
import pygrametl

from dis_etl.extract import get_sale_source
from dis_etl.datetime_dim import build_dim_datetime, get_datetime_key

pgconn = psycopg2.connect(dbname='fklubdw', user='admin@example.com', password="admin", host='localhost')
conn = pygrametl.ConnectionWrapper(connection=pgconn)

dim_datetime = build_dim_datetime(conn)

for row in get_sale_source():
    dt_key = get_datetime_key(dim_datetime, row['timestamp'])

conn.commit()
conn.close()