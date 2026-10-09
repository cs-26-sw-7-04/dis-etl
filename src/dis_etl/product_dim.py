from pygrametl.tables import CachedDimension
from dis_etl.product_utils import decompose_product_row

def build_dim_product(connection) -> CachedDimension:
    return CachedDimension(
        name="dim_product",
        key="id",
        attributes=[
            "product_id",
            "name",
            "price",
            "alcohol_content_ml",
            "active_state",
            "category_major",
            "category_minor",
            "category_sub",
            "category_subsub",
            "valid_from",
            "valid_to",
            "version"
        ],
        lookupatts=["product_id", "version"],
        #keyrefs=["valid_from", ],
        targetconnection=connection,
    )

def time_to_version(foo):
    return 1;

def get_product_key(dim_product: CachedDimension, dim_datetime: CachedDimension, raw_row: dict):
    return dim_product.ensure(decompose_product_row(raw_row, dim_datetime))

def lookup_product_key(dim_product: CachedDimension, product_id: int, datetime: dim_datetime):
    return dim_product.lookup({'product_id': product_id, 'version': time_to_version(datetime)})