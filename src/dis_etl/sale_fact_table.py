"""
fact_sales setup and load logic.
"""

from bisect import bisect_right
from decimal import *
from tqdm import tqdm
from pygrametl.tables import FactTable

from dis_etl.datetime_utils import truncate_to_minute
from dis_etl.extract import get_sale_source
from dis_etl.product_dim import lookup_product_key

# placeholder dim_product key until the real dim_product
# slowly changing dimention is implemented
PLACEHOLDER_PRODUCT_KEY = -1


def build_fact_table_sale(connection) -> FactTable:
    """Returns a sales fact table"""
    return FactTable(
        name="fact_sale",
        measures=["quantity", "price"],
        keyrefs=["dim_member", "dim_product", "dim_datetime"],
        targetconnection=connection,
    )


def fact_sale_grouped(resolve_product, total_sales=None) -> list[dict]:
    """Returns grouped sales"""
    rows = list(get_sale_source())

    # truncate all tiemstamps like in dim_datetime
    for sale in tqdm(rows, total=total_sales, desc="Resolving products", unit="rows"):
        # Resolve the version with the raw, second-precision timestamp
        sale["product_key"] = resolve_product(
            int(sale["product_id"]), sale["timestamp"]
        )
        # Truncate to the minute, like in dim_datetime
        sale["minute"] = truncate_to_minute(sale["timestamp"])

    rows.sort(key=lambda r: (int(r["member_id"]), int(r["product_id"]), r["timestamp"]))

    grouped = []

    for sale in tqdm(rows, desc="Grouping sales", unit="rows"):
        price = Decimal(str(sale["price"]))

        # if grouped not empty and same as previous sale/group
        if (
            grouped
            and grouped[-1]["member_id"] == sale["member_id"]
            and grouped[-1]["product_key"] == sale["product_key"]
            and grouped[-1]["minute"] == sale["minute"]
        ):
            # sale part of previous group
            grouped[-1]["quantity"] += 1
            grouped[-1]["price"] += price
        else:
            # sale part of new group
            sale["quantity"] = 1
            sale["price"] = price
            grouped.append(sale)

    return grouped








def make_resolver(pgconn):
    """Loads all product versions once and resolves (product_id, ts) -> dim_product.id."""
    versions: dict[int, tuple[list, list]] = {}
    with pgconn.cursor() as cur:
        cur.execute(
            "SELECT product_id, id, valid_from FROM dim_product "
            "ORDER BY product_id, valid_from"
        )
        for product_id, key, valid_from in cur:
            froms, keys = versions.setdefault(product_id, ([], []))
            froms.append(valid_from)
            keys.append(key)

    def resolve(product_id: int, ts) -> int:
        if product_id not in versions:
            raise ValueError(f"Product {product_id} not in dim_product")
        froms, keys = versions[product_id]
        i = bisect_right(froms, ts) - 1  # valid_from <= ts < next valid_from
        return keys[max(i, 0)]  # before first version -> first version

    return resolve
