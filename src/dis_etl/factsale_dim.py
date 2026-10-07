"""
fact_sales setup and load logic.
"""

from pygrametl.tables import FactTable


def build_fact_table_sale(connection) -> FactTable:
    """Returns a sales fact table"""
    return FactTable(
        name="fact_sale",
        measures=["quantity", "price"],
        keyrefs=["dim_member", "dim_product", "dim_datetime"],
        targetconnection=connection,
    )
