"""docs :3"""

from datetime import datetime as dt
from datetime import timedelta, timezone

from dis_etl.extract import get_product_categories_source


def get_history(source_row: dict, pricehistory) -> tuple[dt, dt, int, int]:
    """docs :3"""
    relevanthistory = [
        row for row in pricehistory if row["product_id"] == source_row["id"]
    ]
    relevanthistory.sort(key=lambda r: r["changed_on"])

    output = []
    previous_change = dt.fromtimestamp(0, tz=timezone(timedelta(0)))
    i = 1
    for row in relevanthistory:
        output.append((previous_change, row["changed_on"], i, row["price"]))
        previous_change = row["changed_on"]
        i += 1

    output.append(
        (
            previous_change,
            dt.max.replace(tzinfo=timezone(timedelta(0))),
            i,
            source_row["price"],
        )
    )

    # print(f"Getting history of product {source_row['id']}. It has the times of {output}")
    return output


def categorise(productid) -> tuple[str, str, str, str]:
    """docs :3"""
    basecat = [  # noqa: RUF015
        catrow["category"]
        for catrow in get_product_categories_source()
        if catrow["id"] == productid
    ][0]  # we know there's only one line per product

    cat4 = basecat.capitalize()
    cat3 = {
        "Snack": "Snack",
        "Event food": "Event food",
        "Ordinary beer": "Beer",
        "Specialty beer": "Beer",
        "Christmas beer": "Beer",
        "Wine": "Wine",
        "Liquor": "Liquor",
        "Cider": "Cider",
        "Drink": "Drink",
        "Water": "Water",
        "Cocoa": "Cocoa",
        "Soda": "Soda",
        "Ice tea": "Ice tea",
        "Energy drink": "Caffeinated",
        "Coffee": "Caffeinated",
        "Milk": "Dairy",
        "Yoghurt": "Dairy",
        "Juice": "Juice",
        "One-time": "One-time",
        "Repeated": "Repeated",
        "Merch": "Merch",
        "Pant": "Pant",
        "Other physical thing": "Other physical thing",
        "Event stuff": "Event stuff",
        "Other misc": "Other misc",
        "Vitamin water": "Vitamin water",
    }[cat4]
    cat2 = {
        "Snack": "Snack",
        "Event food": "Event food",
        "Beer": "Alcoholic",
        "Wine": "Alcoholic",
        "Liquor": "Alcoholic",
        "Cider": "Alcoholic",
        "Drink": "Alcoholic",
        "Cocoa": "Non-alcoholic",
        "Soda": "Non-alcoholic",
        "Ice tea": "Non-alcoholic",
        "Caffeinated": "Non-alcoholic",
        "Dairy": "Non-alcoholic",
        "Juice": "Non-alcoholic",
        "Water": "Non-alcoholic",
        "Vitamin water": "Non-alcoholic",
        "One-time": "One-time",
        "Repeated": "Repeated",
        "Merch": "Merch",
        "Pant": "Pant",
        "Event stuff": "Physical thing",
        "Other physical thing": "Physical thing",
        "Other misc": "Other misc",
    }[cat3]
    cat1 = {
        "Snack": "Edible",
        "Event food": "Edible",
        "Alcoholic": "Drinkable",
        "Non-alcoholic": "Drinkable",
        "One-time": "Event",
        "Repeated": "Event",
        "Merch": "Merch",
        "Pant": "Miscellaneous",
        "Physical thing": "Miscellaneous",
        "Other misc": "Miscellaneous",
    }[cat2]

    return cat1, cat2, cat3, cat4


def decompose_product_row(source: dict, pricehistory) -> list:
    """docs :3"""
    cat1, cat2, cat3, cat4 = categorise(source["id"])
    return [
        {
            "product_id": source["id"],
            "name": source["name"],
            "price": price / 100,
            "alcohol_content_ml": source["alcohol_content_ml"],
            "active_state": "active" if source["active"] else "inactive",
            "category_major": cat1,
            "category_minor": cat2,
            "category_sub": cat3,
            "category_subsub": cat4,
            "untildate": valid_to,
        }
        for (valid_from, valid_to, version, price) in get_history(source, pricehistory)
    ]
