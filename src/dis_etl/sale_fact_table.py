"""
fact_sales setup and load logic.
"""

from pygrametl.tables import FactTable

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
    rows.sort(key=lambda r: (int(r["member_id"]), int(r["product_id"]), r["timestamp"]))

    groupedsale = []
    prev_sale = None

    for current_sale in rows:
        if prev_sale is None:
            current_sale["quantity"] = 1
            current_sale["price"] = int(current_sale["price"])
            groupedsale.append(current_sale)
            prev_sale = current_sale
            continue

        deltatime = (current_sale["timestamp"] - prev_sale["timestamp"]).total_seconds()

        if (
            current_sale["member_id"] == prev_sale["member_id"]
            and current_sale["product_id"] == prev_sale["product_id"]
            and deltatime <= 10
        ):
            groupedsale[-1]["quantity"] += 1
            groupedsale[-1]["price"] = int(current_sale["price"])

        else:
            current_sale["quantity"] = 1
            current_sale["price"] = int(current_sale["price"])
            groupedsale.append(current_sale)
            prev_sale = current_sale

    return groupedsale
