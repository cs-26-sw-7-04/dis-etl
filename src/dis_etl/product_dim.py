from pygrametl.tables import SlowlyChangingDimension
import pygrametl
from dis_etl.product_utils import decompose_product_row
from datetime import datetime as dt

def build_dim_product(connection) -> SlowlyChangingDimension:
    return SlowlyChangingDimension(
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
            #"valid_from",
            "valid_to",
            "version"
        ],
        lookupatts=["product_id"],
        #keyrefs=["valid_from", ],
        targetconnection=connection,
        versionatt='version',
        #fromatt='valid_from',
        toatt='valid_to',
        tofinder=pygrametl.datetimereader('untildate')
    )

def time_to_version(foo):
    return 1;

def get_product_key(dim_product: SlowlyChangingDimension, oldprices: dict, raw_row: dict):
    return [dim_product.scdensure(version) for version in decompose_product_row(raw_row, oldprices)]

def lookup_product_key(dim_product: SlowlyChangingDimension, product_id: int, asof: dt):
    #print(f"Looking up product on datetime {asof}!!!!")
    return dim_product.lookupasof({'product_id': product_id}, when=asof, inclusive=(True, False)) #Cannot be cached