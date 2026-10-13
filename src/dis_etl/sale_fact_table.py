"""
fact_sales setup and load logic.
"""

from pygrametl.tables import FactTable

from dis_etl.datetime_utils import truncate_to_minute
from dis_etl.extract import get_sale_source

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


def fact_sale_grouped():
    """Returns grouped sales"""
    rows = list(get_sale_source())

    # truncate all tiemstamps like in dim_datetime
    for sale in rows:
        sale["timestamp"] = truncate_to_minute(sale["timestamp"])

    rows.sort(key=lambda r: (int(r["member_id"]), int(r["product_id"]), r["timestamp"]))

    grouped = []

    for sale in rows:
        price = int(sale["price"]) / 100 # To DKK and not ears 👂

        # if goruped not empty and same as previous sale/group
        if (grouped and grouped[-1]["member_id"] == sale["member_id"]
                    and grouped[-1]["product_id"] == sale["product_id"]
                    and grouped[-1]["timestamp"] == sale["timestamp"]
        ):
            # sale part of previous group
            grouped[-1]["quantity"] += 1
            grouped[-1]["price"] += price
        else:
            # sale part of new gorup
            sale["quantity"] = 1
            sale["price"] = price
            grouped.append(sale)

    return grouped
