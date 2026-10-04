"""Extracting data from datasources"""
import datetime
import pygrametl.datasources


def parse_timestamp_utc(s: str) -> datetime.datetime:
    """Parse a source timestamp with its offset, then convert to UTC."""
    dt = datetime.datetime.fromisoformat(s)        # e.g. '1996-11-19 17:11:51+01'
    return dt.astimezone(datetime.timezone.utc)    # now tz-aware and in UTC


def parse_bool(s: str) -> bool:
    """Interprets the boolean in strign f or t from datasource"""
    return s == "t"


member_source = pygrametl.datasources.TypedCSVSource(
    f=open("./data/member.csv", "r", 16384, encoding="utf-8"),
    casts={
        "id": int,
        "active": parse_bool,
        "year": lambda s: int(s) if s else None,   # blank handled here, mapped to sentinel later
        "gender": str,
        "want_spam": parse_bool,
        "balance": int, # Øre
        "undo_count": int,
    },
    delimiter=";"
)


product_source = pygrametl.datasources.TypedCSVSource(
    f=open('./data/product.csv', 'r', 16384, encoding="utf-8"),
    casts={
        'id': int,
        'name': str,
        'price': int, # Øre
        'active': parse_bool,
        'deactivate_date': lambda s: parse_timestamp_utc(s) if s else None,
        'quantity': int,
        'alcohol_content_ml': lambda s: float(s) if s else 0.0,
        'start_date': lambda s: parse_timestamp_utc(s) if s else None,
    },
    delimiter=';'
)


oldprice_source = pygrametl.datasources.TypedCSVSource(
    f=open('./data/oldprice.csv', 'r', 16384, encoding="utf-8"),
    casts={
        'id': int,
        'product_id': int,
        'price': int, # Øre
        'changed_on': parse_timestamp_utc,
    },
    delimiter=';'
)


sale_source = pygrametl.datasources.TypedCSVSource(
    f=open('./data/sale.csv', 'r', 16384, encoding="utf-8"),
    casts={
        'id': int,
        'member_id': int,
        'product_id': int,
        'room_id': int,
        'timestamp': parse_timestamp_utc,
        'price': int, # Øre
    },
    delimiter=';'
)


category_source = pygrametl.datasources.TypedCSVSource(
    f=open('./data/category.csv', 'r', 16384, encoding="utf-8"),
    casts={
        'id': int, 
        'name': str
    },
    delimiter=';'
)


product_categories_source = pygrametl.datasources.TypedCSVSource(
    f=open('./data/product_categories.csv', 'r', 16384, encoding="utf-8"),
    casts={
        'id': int, 
        'product_id': int, 
        'category_id': int
    },
    delimiter=';'
)


room_source = pygrametl.datasources.TypedCSVSource(
    f=open('./data/room.csv', 'r', 16384, encoding="utf-8"),
    casts={
        'id': int, 
        'name': str, 
        'description': str
    },
    delimiter=';'
)


payment_source = pygrametl.datasources.TypedCSVSource(
    f=open('./data/payment.csv', 'r', 16384, encoding="utf-8"),
    casts={
        'id': int, 
        'member_id': str, 
        'timestamp': parse_timestamp_utc,
        'amount': int
    },
    delimiter=';'
)
