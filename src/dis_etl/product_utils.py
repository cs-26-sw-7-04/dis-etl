from dis_etl.datetime_dim import get_datetime_key
from datetime import datetime as dt

def decompose_product_row(source: dict, dim_datetime) -> dict:
    return {
        "product_id": source["id"],
        "name": source["name"],
        "price": source["price"]/100,
        "alcohol_content_ml": source["alcohol_content_ml"],
        "active_state": "active" if source["active"] else "inactive",
        "category_major": "TEMPORARY",
        "category_minor": "TEMPORARY",
        "category_sub": "Temporary.",
        "category_subsub": "TEMPORARY!",
        "valid_from": get_datetime_key(dim_datetime, dt.fromtimestamp(0)),
        "valid_to": get_datetime_key(dim_datetime, dt.fromtimestamp(0)),
        "version": 1
    }