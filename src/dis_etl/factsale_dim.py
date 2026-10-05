from pygrametl.tables import FactTable


def build_fact_sale(connection) -> FactTable:

    return FactTable(
    name="fact_sale",
    measures=["quantity",
               "price"],
    keyrefs=["dim_member"
             ,"dim_product"
             ,"dim_datetime"]    
    )